import logging
from flask import render_template, request

from config import USERNAME, PASSWORD, SUBSCRIBER_ID
from app import app
from api import BancboxClient

logger = logging.getLogger(__name__)

api = BancboxClient(USERNAME, PASSWORD, SUBSCRIBER_ID)

@app.route('/')
def index():
    """
    Renders the main client page - containing a form to add new clients, as
    well as a list of existing clients.
    """
    try:
        # Retrieve a list of active clients from the BancBox API for 
        # the right side bar.
        active_clients = api.get_active_clients()
    except Exception, e:
        active_clients = []
        logger.error('Error retrieving active clients: %s', e)
    return render_template('index.html', active_clients=active_clients)

@app.route('/clients/create/', methods=['POST'])
def create():
    """
    Accepts a request to create a new client, renders a success/failure
    page based on the response from BancBox
    """
    form = request.form
    try:
        # create a new BancBox client from the input form
        resp = api.create_client(form)
    except Exception, e:
        logger.error('Error creating new client: %s', e)
        return render_template('created.html', error=e.message)

    if resp.status == 1:
        # If the create request was successful, let's render a success
        # message with some data about the new client and a link to the
        # detail page
        new_client = {
            'firstName': form['firstName'],
            'lastName': form['lastName'],
            'clientId': resp.clientId
            }
        return render_template('created.html', new_client=new_client)
    else:
        # If an error was returned by BancBox, let's render it
        if hasattr(resp, 'errors') and hasattr(resp.errors, 'message'):
            message = resp.errors.message
        else:
            message = "Error creating new client."
        return render_template('created.html', error=message)

@app.route('/clients/<client_id>/detail/')
def detail(client_id):
    """
    Renders a client detail page - fetches the client with the specified Id
    from BancBox and displays the data for that client.
    """
    try:
        # Fetch client details from the BancBox api and render
        clientId = { 'bancBoxId': client_id }
        request_params = {'subscriberId': subscriber_id, 'clientId': clientId}
        results = api.service.getClient(request_params) 
        client = results.client
    except Exception, e:
        logger.error('Error retrieving client [%s]: %s', client_id, e)
        client = {}
    return render_template('detail.html', client=client)
