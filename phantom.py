# coding: utf-8

import tempfile
import subprocess
import md5
import datetime


def html_to_pdf(html):
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
	pdf_tmp	 = tempfile.NamedTemporaryFile(mode='r+b', suffix='.pdf')
		
	# edit rasterize_pdf to change size/header+footer settings
	# maybe expose some options here if we need them
	phantom_cmd = [ 'phantomjs',
					'phantom-scripts/rasterize_pdf.js',
					'%s' % html_tmp.name,
					'%s' % pdf_tmp.name]

	try:
		html_tmp.write(html.encode('utf8'))
		html_tmp.flush()

		print subprocess.call(phantom_cmd)

		return pdf_tmp.read()

	finally:
		html_tmp.close()
		pdf_tmp.close()

def url_to_pdf(url):
        """Runs phantomjs in a subprocess to render a URL into a pdf

        Args:
                url: URL to render

        Returns:
                File handle to temp file of pdf

        Raises:
                OSError: An error occured in running the phantomjs subprocess

        """

        # get a file name. This has a TOC/TOU problem but it shouldn't matter 
        pdf_tmp  = tempfile.NamedTemporaryFile(mode='w+b', suffix='.pdf',dir='generated_pdfs').name
        pdf_tmp.close()
        
        # edit rasterize_pdf to change size/header+footer settings
        # maybe expose some options here if we need them
        phantom_cmd = [ 'phantomjs',
                        'phantom-scripts/rasterize.js',
                        url,
                        pdf_tmp]

        try:
            print subprocess.call(phantom_cmd)
            pdf_file = file(pdf_tmp,'rb')
        except:
            return pdf_file
        else:
            pdf_file.close()
