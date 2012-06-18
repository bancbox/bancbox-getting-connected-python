bancbox-getting-connected-python
================================

Getting Connected with BancBox APIs using Python

Introduction:
	This is a sample application to demonstrate how to access and interact with
	the BancBox API. This sample application demonstrates how to use several of
	the methods provided by the API: 
		
		- createClient: used to register new BancBox clients
		- searchClients: used to query the Bancbox for registered clients
		- getClient: used to retrieve details about a BancBox client

Requirements:
	- A working Python installation
		- Sample application was tested on Python 2.7.2
		- Python 2.5 or greater recommended
	
	- Recommended Python packages:
		- virtualenv
		- pip

Quick Start
	This is a Flask application - simply run the Flask application to get
	started.

		1. If you want to run this in a virtualenv, create a new virtualenv (Or
		skip to step 3):
			
			virtualenv --no-site-packages env

		2. Drop the application folder into the new virtual env

		3. Install the requirements:

			pip install -r sample_app/requirements.txt

			- Or, individually -

			pip install Flask
			pip install suds

			(If not using a virtual env, sudo may be required, e.g.: 
			sudo pip install Flask)

		4. Run the development server:
			
			python runserver.py

		5. Open the app in your browser by going to the following URL:

			http://127.0.0.1:5000

Installation:
	Begin by installing the required Python packages in the requirements.txt 
	file.
		
		I suggest running the application within a Virtual Environment
		via virtualenv. (http://pypi.python.org/pypi/virtualenv). Simply
		install the requirements within the vitual env by issuing the 
		following commend: pip install -r requirements.txt

	Once the required packages are installed, you can run the application.

Running
	To run the sample application, execute the runserver.py script to start
	the built-in development server: 
	
		python runserver.py

	By default, the development server runs on port 5000. To access the
	application, go to the following URL in a web browser:

		http://127.0.0.1:5000

Implementation
	The sample application is built using several Python libraries:
		- Flask
		- SUDS

	Flask is a lightweight (micro) web framework designed for quick and
	easy web application development. Flask was chosen for this sample
	application because of the minimal amount of code needed to produce
	a functional application. URL routing, request handling, and template
	rendering are all very simple. The best place to learn about Flask
	is by reading the excellent Flask documentation located here: 
		
		http://flask.pocoo.org/
		
	SUDS is a generic Python client for accessing SOAP web services. SUDS
	was chosen for this sample application for several reasons:  
		1. Working with XML in Python is not as easy as in other popular 
		languages - working with SOAP web services is even harder to do by 
		hand. Using a client library can eliminate a lot of this complexity. 
		Unless you're working on an application with a lot of specific
		requirements that prevent the use of a generic library, this is 
		likely much simpler than writing your own wrapper.

		2. There are few functional, well-maintained, Pythonic SOAP client
		libraries for Python. SUDS is currently the most popular, the most
		Pythonic, and most actively maintained library available.
		
	SUDS documentation can be found here:

		https://fedorahosted.org/suds/

Flask Primer
	Here is a brief explanation of how this Flask application is configured:

		Creating a flask app is very simple:
				
				from flask import Flask
				app = Flask(__name__) # create an application

				# create a basic view
				@app.route('/')
				def index():
				    return 'Hello, World!'

				if __name__ == '__main'':
					# run the application (built in development server)
					app.run()

		The example application above would certainly fit in a single python
		file. This, however, is not practical, so this sample application is
		organized as a Python package.

		At the top level of the application is a runserver.py script. This
		script imports our Flask application and runs the built-in development
		web server. The Flask application lives within a package called 
		sample_app in the same folder. The Flask application is defined in the 
		app.py module.
		
		Also in our application module are several other modules:
			- views.py: contains the views we've defined for our application,
			  along with the URL routes we've defined. Views and URLS have been
			  defined for displaying a client list and creation form, creating 
			  a new client, and displaying client details. URLS are defined in
			  a Flask application using the 'route' decorator as shown above. 
			  The views in our sample application render HTML templates via
			  Flask's render_template function. See below for a further
			  explanation of Flask views and templates

			- api.py: contains classes for accessing the BancBox API. See the
			  SUDS primer below for more information

		URL Routing

			Given a Flask application, URL routing and view creation is 
			done via a decorator:

				app = Flask(__name__) # creates an application

				@app.route('/clients/create/') defines a url route
				def create():
					# defines a view for the create url
					...

		Rendering templates

			This sample application contains 3 templates: A form for creating
			new clients, a page for displaying information about a newly-created
			client, and a page for displaying client detail. We render these
			in each view using Flask's render_template function.

			Additionally, we pass custom information to these templates to 
			display custom data based on actions performed. For example, we 
			render specific client data such as client name and address. This
			is done via the Flask templating framework (powered by Jinja2). 
			Documentation for this is located here: 
				http://flask.pocoo.org/docs/quickstart/#rendering-templates
			
			Templates are located within the application module - they live in 
			a directory called 'templates'. Rendering a template is simple:

				@app.route('/myurl')	
				def view_func():
					 return render_template('my_template.html')

			This will look in the templates directory for a file called
			'my_template.html' and render it.

			To pass data to a template to be rendered, simply pass the
			arguments by name into the render_template function:

				@app.route('/myurl')
				def view_func():
				    client = api.get_client()
					 return render_template('my_template.html', client=client)

			To access this item within a template, simply use the Jinja
			templating language:

				<html>
				<body>
					{% if client %}
					    <div id='client_name'> {{ client.name }} </div>
					{% endif %}
				</body>
				</html>

			This markup will print the name attribute of the client object if the
			client object is defined and not empty - that is, if you pass a valid
			client to the render template function, the client's name will be 
			printed inside a div.

			For further examples, see the Flask and Jinja documentation.


SUDS Primer
	The SUDS library contains generic functionality for accessing most
	SOAP-complaint web services. When the default functionality is not
	sufficient, SUDS contains a plugin facility for extending core SUDS
	functionality to fit your needs. This sample application creates 
	a light wrapper around a basic SUDS client, and uses a simple plugin
	to modify SUDS to be compliant with the BancBox API.

	To create a SUDS client, simple instantiate the SUDS Client class and
	pass it some data about the webservice you want to access:

		import suds.client

		client = suds.client.Client(url='http://api.mysite.com/service?wsdl')

	When the location of the WSDL for the web service is provided, SUDS
	will parse the WSDL and return a client that knows how to interact
	with the web service. Detailed documentation can be found here:
		
		https://fedorahosted.org/suds/wiki/Documentation

	After parsing the WSDL, the client above will have two important
	attributes:
		
		client.service: a proxy object for accessing the webservice
			
			If the service defines a createClient method, it would be called
			in the following manner:

			client.service.createClient(args)

		client.factory: a factory object used to create objects defined by the
		WSDL

	The BancBox API requires requests to be authenticated. This is done by
	passing a WSSE SOAP header as part of the request. SUDS supports WSSE
	out of the box:

		import suds.wsse

		security = suds.wsse.Security()
		token = suds.wsse.UsernameToken(username, password)
		security.tokens.append(token)
		client.set_options(wss=security)


	This code creates a WSSE header and sets it as an option on the client 
	object. The client will then pass the headers along with other request 
	data whenever a request is made.

	Though SUDS supports basic WSSE out of the box, it does not construct
	a header that the BancBox API will accept. A little modification is needed
	to authenticate requests to BancBox. This is done via a SUDS plugin.
	The plugin within the sample app is located in the api.py module - it is 
	called PasswordTypePlugin. It simple alters the password element in the 
	header by defining a Type attribute: 
		
		class PasswordTypePlugin(suds.plugin.MessagePlugin)
		    def marshalled(self, context):
		        password = context.envelope.childAtPath('Header/Security/UsernameToken/Password')
			     password.set('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

	An instance of this plugin in passed to a new client instance when it
	is created:

		client = suds.client.Client(url='http://api.mysite.com/service?wsdl',
		        plugins=[PasswordTypePlugin()])

	For more detailed information about SUDS functionality, refer to the SUDS
	documentation.

