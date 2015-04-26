

How to configure 
===============

First register app on your facebook account. By doing that you'll get app id. Also you'll need to setup redirect URL to localhost to 
application can work properly. 

Rename template.py.template to template.py and fill in APP ID 

then you need to get token by using 

	archiver --action token

and then go to given url and copy & save token from the url. Token will be given as one of the parameters in the url. 

for more information, type 

	archiver --help
