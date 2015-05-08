# coding: utf-8

import os
import logging
import flask
import json
import flask_config
import phantom

def to_bool(val):
     if isinstance(val, basestring):
         if val == '1' or val.lower() == 'true':
             return True
         return False
     return bool(val)

app = flask.Flask(__name__)
app.static_folder = "public"
app.SEND_FILE_MAX_AGE_DEFAULT = 0
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] is_bool(os.environ.get('APP_MODE_DEBUG', False))
	
@app.route('/')
def pdf():
	
	
	"""Returns html that is useful for understanding, debugging and extending
	the charting API"""

	return file('public/pdf.html').read()
			
@app.route('/html-to-pdf', methods=['POST'])
def html_to_pdf():
	
	"""Takes an HTTP POST with html, renders a pdf using phantomjs and returns
	a pdf.

	Example use with jQuery:

		$.post('/html-to-pdf', {'html': HTML})

	"""
	html = flask.request.form.get('html', '')
	title = 'html2pdf'

	try:
		pdf_data = phantom.html_to_pdf(html)
	except OSError as e:
		# Reraise the error so flask can log it
		raise e

	if pdf_data:
		response = flask.make_response(pdf_data)
		response.headers['Cache-Control'] = 'no-cache'
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = "attachment;filename=%s.pdf"%title
		return response

	else:
		flask.abort(400)

@app.route('/url-to-pdf', methods=['POST'])
def url_to_pdf():
        """Takes an HTTP POST with a url, renders a pdf using phantomjs and returns
        a pdf.

        Example use with jQuery:

                $.post('/url-to-pdf', {'url': url})

        """
        url = flask.request.form.get('url', '')
        title = 'url2pdf'

        try:
                pdf_file = phantom.url_to_pdf(url)
        except OSError as e:
                # Reraise the error so flask can log it
                raise e
       
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0, os.SEEK_SET)
        if size:
                return send_file(pdf_file, 
                                 mimetype='application/pdf',
                                 attachment_filename='{0}.pdf'.format(pdf_file.name.split(os.sep)[-1])
                        )        
        else:
                flask.abort(400)

if __name__ == '__main__':
	# Set up logging to stdout, which ends up in Heroku logs
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	app.logger.addHandler(stream_handler)

	app.debug = True
	app.run(host='0.0.0.0', port=flask_config.port)
