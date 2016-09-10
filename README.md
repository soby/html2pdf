= html2pdf =

Easily convert HTML into a PDF.

Deploy locally or on a server to create a PDF service.

Clone this reposity locally. To run this locally, install PhantomJS first. 

Next, you need to run:

virtualenv --distribute venv

This will create a directory for all your virtual files. Next activate the virtual enviornment by typing:

source venv/bin/activate

Once you are activated, you need to install all the dependencies by typing:

pip install -r requirements.txt

This will install all the needed files and other code.

Then you can type:

python run.py

This will run the flask server on http://0.0.0.0:5000 by default.

If you want to learn more about deploying this on heroku, you can read:

http://optional.is/required/2014/06/12/pdf-creation-from-html-service/

( Don't forget to do this: heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git)
You can also automatically deploy to Heroku by clicking the button
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
