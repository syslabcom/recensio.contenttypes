"""
Helper utilities for recensio.contenttypes
"""
from tempfile import mkstemp
import os
import subprocess

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


class RunSubprocess:
    """
    largely copied from ploneformgen's gpg calls (via wv.pageturner)
    """
    def __init__(self, program_name, extra_paths=[]):
        self.program = which(program_name, extra_paths)
        if self.program is None:
            raise IOError, "Unable to find the %s program" % program_name

    def __call__(self, input_data, input_params="", output_params=""):
        """
        E.g. Convert a Word doc file contained in filedata into a pdf
        """
        _, input_path = mkstemp()
        file_obj = open(input_path, 'w')
        file_obj.write(input_data)
        file_obj.close()

        _, output_path = mkstemp()

        cmd = [self.program] + input_params.split() + [input_path] +\
              output_params.split() + [output_path]
        stdoutdata, stderrdata = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ).communicate()

        if stderrdata:
            return Exception(stderrdata)

        output_data = open(output_path)

        return output_data.read()

wvPDF = RunSubprocess("wvPDF")
