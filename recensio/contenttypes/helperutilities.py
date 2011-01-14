"""
Helper utilities for recensio.contenttypes
"""
import tempfile
import os
import subprocess
import logging

from Products.Five.browser.pagetemplatefile import PageTemplateFile

log = logging.getLogger('recensio.theme/helperutilities.py')

def which(program_name, extra_paths=[]):
    """
    Return the full path to a program
    """
    paths = []
    if os.environ.has_key('PATH'):
        paths = os.environ['PATH']
        paths = paths.split(os.pathsep)
    paths = paths + extra_paths
    for dir in paths:
        full_path = os.path.join(dir, program_name)
        if os.path.exists(full_path):
            return full_path
    return None

# http://tools.cherrypy.org/wiki/ZPT
class SimpleZpt(PageTemplateFile):
    """ Customise ViewPageTemplateFile so that we can pass in a dict
    to be used as the context """
    def pt_getContext(self, args=(), options={}, **kw):
        rval = PageTemplateFile.pt_getContext(self, args=args)
        options.update(rval)
        return options


class SubprocessException(Exception):
    """For exceptions from RunSubprocess"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

def SimpleSubprocess(*cmd, **kwargs):
    """
        Run a sub process, return all output, retval[0] is stdout,
        retval[1] ist stderr
        If the process run failed, raise an Exception
        cmd imput arg is supposed to be a list with the command
        and the passed arguments
    """
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,\
            stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
    except OSError, e:
        raise RuntimeError(str(e))

    returncode = process.returncode

    if returncode not in kwargs.get('exitcodes', [0]):
        raise RuntimeError(" ".join([str(returncode), stderrdata]))

    return stdoutdata, stderrdata

class RunSubprocess:
    """Wrapper for external command line utilities

    Creates temporary files/directories as required and helps remove
    them afterwards.

    Usage:
    $ pdftk /path/to/file.pdf burst output /path/to/output_%%04d.pdf
    gen_thumbs = RunSubprocess("pdftk")
    gen_thumbs.create_tmp_input(suffix=".pdf", data=<pdf data>)
    gen_thumbs.create_tmp_output_dir()
    gen_thumbs.output_params = "burst output"
    gen_thumbs.run()
    if gen_thumbs.errors == None:
        result = gen_thumbs.output_path
    gen_thumbs.clean_up()
    """
    def __init__(self, program_name, extra_paths=[], input_path="",
                 input_params="", output_params="", output_path=""):
        self.program_name = program_name
        self.program = which(program_name, extra_paths)
        if self.program is None:
            raise SubprocessException("Uable to find the %s program" % (
                    program_name))
        self.tmp_input = None
        self.tmp_output = None
        self.tmp_output_dir = None
        self.input_path = input_path
        self.input_params = input_params
        self.output_params = output_params
        self.output_path = ""
        self.errors = ""
        self.cmd = ""

    def _create_tmp_file(self, prefix="", suffix="", data=None):
        """Create a temporary file as input for the command"""
        fd, path = tempfile.mkstemp(prefix=prefix, suffix=suffix)
        tmp_file = os.fdopen(fd, "w")
        if data:
            tmp_file.write(data)
        tmp_file.close()
        return path

    def create_tmp_input(self, prefix="", suffix="", data=None):
        self.input_path = self._create_tmp_file(prefix=prefix, suffix=suffix,
                                               data=data)

    def create_tmp_ouput(self, prefix="", suffix="", data=None):
        self.tmp_output = self._create_tmp_file(prefix=prefix, suffix=suffix,
                                                data=data)

    def create_tmp_output_dir(self, **kw):
        self.tmp_output_dir = tempfile.mkdtemp(**kw)

    def run(self, input_params="", input_path="", output_params="",
            output_path=""):
        """Run the command"""

        if input_params != "":
            self.input_params = input_params

        if input_path != "":
            self.input_path = input_path
        elif self.input_path == "":
            self.input_path = self.tmp_input

        if output_params != "":
            self.output_params = output_params

        if output_path != "":
            self.output_path = output_path
        elif self.output_path == "":
            self.output_path = True and self.tmp_output or self.tmp_output_dir

        self.cmd = [self.program] + self.input_params.split() +\
            [self.input_path] + self.output_params.split() + [self.output_path]
        log.info("Running the following command:\n %s" % " ".join(self.cmd))

        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE,\
            stderr=subprocess.PIPE)

        stdoutdata, stderrdata = process.communicate()

        returncode = process.returncode

        if returncode:
            raise RuntimeError(" ".join([str(returncode), stderrdata]))

        if stderrdata:
            if "Error" in stderrdata:
                log.error(stderrdata)
            else:
                log.info(stderrdata)

    def clean_up(self):
        """Remove any temporary files which have been created"""
        for tmp in [self.tmp_input, self.tmp_output]:
            if tmp is not None and os.path.exists(tmp):
                os.remove(tmp)

        if self.tmp_output_dir is not None:
            tmp_dir = self.tmp_output_dir
            for tmp_file in os.listdir(tmp_dir):
                os.remove(os.path.join(tmp_dir, tmp_file))
            os.removedirs(tmp_dir)
