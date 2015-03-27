
from facepy import GraphAPI 

from .inbox import Inbox

from .template import APP_ID

class Me(object):
    
    def __init__(self, token):
        self.api = GraphAPI(oauth_token = token)

    def get_inbox(self):
        """
        Returns Inbox objects representing inbox of account
        """
        return Inbox(self.api.get("/me/inbox"))

    def get_token_uri():
        """
        Returns URL for getting tokens 
        """
        uri = "https://www.facebook.com/dialog/oauth?client_id=%s" % APP_ID 
        uri += "&scope=read_mailbox&redirect_uri=https://localhost&response_type=token"
        return uri 
