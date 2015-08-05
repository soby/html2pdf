# coding: utf-8

import os
import tempfile
import subprocess


def html_to_pdf(html, session=None, header=None):
    """Runs phantomjs in a subprocess to render html into a pdf 

	Args:
		html: String of html to render

	Returns:
		The pdf data in a string. If phantomjs doesn't like the html,
		this string can end up empty.

	Raises:
		OSError: An error occured in running the phantomjs subprocess

	"""

    # TODO: Use stdin and stdout instead of tempfiles, as Heroku makes no
    # guarantees about tempfiles not being destroyed mid-request. This may
    # require use of phantomjs version 1.9, which (as of 2013-3-2) hasn't been
    # released
    html_tmp = tempfile.NamedTemporaryFile(mode='w+b', dir="phantom-scripts", suffix='.html')
    html_tmp.write(html)
    html_tmp.seek(0)
    
    return url_to_pdf(html_tmp.name, session, header)


def url_to_pdf(url, session=None, header=None):
        """Runs phantomjs in a subprocess to render a URL into a pdf

        Args:
                url: URL to render

        Returns:
                File handle to temp file of pdf

        Raises:
                OSError: An error occured in running the phantomjs subprocess

        """

        # get a file name. This has a TOC/TOU problem but it shouldn't matter 
        pdf_tmp  = tempfile.NamedTemporaryFile(mode='w+b', suffix='.pdf', delete=True, dir='generated_pdfs').name
        
        phantom_cmd = [ 'phantomjs',
                        '--ignore-ssl-errors=true',
                        'phantom-scripts/rasterize.js',
                        url,
                        pdf_tmp]
        if session:
            phantom_cmd.append("--session")
            phantom_cmd.append('%s' % session)
        if header:
            phantom_cmd.append("--header")
            phantom_cmd.append('%s' % header.encode('base64').replace('\n',''))
            
        ret = subprocess.call(phantom_cmd)
        if ret:
            print 'Call to phantomjs failed'
            return None
        try:
            os.stat(pdf_tmp)
        except OSError:
            print 'File not created'
            return None
        try:
            size = os.path.getsize(pdf_tmp)
        except:
            print 'Could not get file size'
            return None
        else:
            if size:
                print 'Returning file of %s size' % size
                return file(pdf_tmp,'rb')
            else:
                print 'Empty file created'
                return None
