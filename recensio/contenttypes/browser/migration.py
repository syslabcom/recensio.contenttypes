from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from recensio.contenttypes.adapter.reviewpdf import ReviewPDF
from recensio.contenttypes import helperutilities 
from time import time, clock, strftime
from plone.app.blob.field import ImageField



TYPES = ['Presentation Online Resource'
        , 'Presentation Article Review'
        , 'Presentation Collection'
        , 'Review Journal'
        , 'Presentation Monograph'
        , 'Review Monograph'
        ]

class migratePagePreview(BrowserView):
    
    def mklog(self):
        """ helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write
        def log(msg, timestamp=True):
            if timestamp:
                msg = strftime('%Y/%m/%d-%H:%M:%S ') + msg
            write(msg)
        return log
        
    def __call__(self):
        helperutilities.RUN_SHELL_COMMANDS = True
        log = self.mklog()
        log('converting preview images...')
        IF = ImageField()
        
        cat = self.context.portal_catalog
        results = cat(Language='all', portal_type=TYPES, b_size=100000)
        
        log(str(len(results))+'\n')
        for result in results:
            try:
                ob = result.getObject()
            except AttributeError:
                continue
            if not hasattr(ob, 'pagePictures') or len(ob.pagePictures)==0:
                log("NOTFOUND: %s has no pagePictures\n" % result.getPath())
                continue
            first = ob.pagePictures[0]
            if type(first) == type(IF):
                continue

            # wrap as blobfield
            newpics = []
            for pic in ob.pagePictures:
                NF = ImageField()
                NF.set(ob, pic)
                newpics.append(NF)
            ob.pagePictures = newpics
            
            log("Success: %s converted\n" % result.getPath())
                
        return
        
        
        
# Code to kill old pagePictures from history
# PH = portal.portal_historiesstorage
# REP = PH._getZVCRepo()
# cnt = 0
# for zvh in REP.objectValues():
#   for vid in zvh.getVersionIds():
#   data = zvh.getVersionById(vid)._data
#   wob = data.getWrappedObject()
#   if not hasattr(wob, 'object'):
#       continue
#   rob = wob.object
#   if hasattr(rob, 'pagePictures'):
#     pp = rob.pagePictures
#     if len(pp)>0 and type(pp[0]) == type(''):
#       print "found one"
#       rob.pagePictures = []
#       rob._p_changed = 1
#       
#       