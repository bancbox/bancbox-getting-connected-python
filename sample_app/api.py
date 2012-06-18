import uuid
import suds.client
from suds.plugin import MessagePlugin
from suds.wsse import Security, UsernameToken

from config import WSDL_LOCATION, API_URL


class PasswordTypePlugin(MessagePlugin):
    """
    A SUDS `MessagePlugin` that will form a proper WSSE header for access to
    the BancBox API
    """
    def marshalled(self, context):
        # Grab the WSSE Password 
        password = context.envelope.childAtPath('Header/Security/UsernameToken/Password')

        # Set a valid Type parameter on the WSSE Password
        password.set('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

class BancboxClient(suds.client.Client):
    """
    A light wrapper around the SUDS.Client class to make authentication easier

    SUDS handles WSSE natively, but does not form a header exactly as the
    BancBox API expects, so we use a plugin - `PasswordTypePlugin` (defined 
    above) - to form a proper header.

    Documentation for SUDS can be found here: https://fedorahosted.org/suds/
    """
    def __init__(self, username, password, subscriber_id):
        """
        Parameters:
            :param username: - Username for accessing the BancBox api. This should 
            be an email address

            :param password: - Password for access the BancBox api.
        """
        # Initialize the suds Client
        super(BancboxClient, self).__init__(url=WSDL_LOCATION, location=API_URL,
                plugins=[PasswordTypePlugin()])

        # Set WSSE security headers
        # Create a new SUDS Security object
        security = Security()

        # Create a WSSE UsernameToken with the supplied username and password
        token = UsernameToken(username, password)

        # Add the token to the Security object
        security.tokens.append(token)

        # Set the security settings on the SUDS Client
        self.set_options(wsse=security)

        self.subscriber_id = subscriber_id


    def get_active_clients(self):
        """
        Returns a list of active clients from BancBox

        :return: a `list` of client objects
        """

        # Create a new `clientStatus` object
        status = self.factory.create('clientStatus')

        # form a search request:
        # Here, we're only searching for clients with a status = ACTIVE
        search_params = {
            'subscriberId': self.subscriber_id,
            'status': status.ACTIVE
        }

        # Perform the search
        results = self.service.searchClients(search_params)

        # Return any clients returned by the BancBox API
        return results.clients

    def create_client(self, form):
        """
        Create a new BancBox Client

        :param form: a `dict` (or dictionary-like) object containing client
        data

        :return: A `createClientResponse`
        """
        # First, filter out any blank form values
        client_info = dict([(k,v) for k,v in form.iteritems() if v])

        # Pull the client address info from the form
        # create a separate address object
        address = {}
        address['line1'] = client_info.pop('addr_line_1')
        address['line2'] = client_info.pop('addr_line_2', None) #optional
        address['city'] = client_info.pop('city')
        address['state'] = client_info.pop('state')
        address['zipcode'] = client_info.pop('zipcode')

        # Add the addres to the create request
        client_info['address'] = address

        # Form a basic request: a subscriberId is always required
        request_params = {
            'subscriberId': self.subscriber_id,
            'referenceId': uuid.uuid4() # a unique id
        }

        # Add the client data to the request
        request_params.update(client_info)
        resp = self.service.createClient(request_params)
        return resp

