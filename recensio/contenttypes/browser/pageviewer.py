from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Pageviewer(BrowserView):
    """Views a review's page images (generated from pdf)"""

    # template = ViewPageTemplateFile('pageviewer.pt')

    def __call__(self):
        return self.showpages()  # self.template()

    def showpages(self):
        # html = ''
        html = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n<head></head>\n<body>\n'
        for i in range(self.context.get_no_pages() + 1)[1:]:
            html = (
                html
                + '    <div>\n      <img src="'
                + self.context.absolute_url()
                + "/get_page_image?no:int=%d" % i
                + '" alt="Review page %d">' % i
                + "\n    </div>\n"
            )
        html = html + "</body>\n</html>\n"

        return html
