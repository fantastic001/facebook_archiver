
from facepy import GraphAPI 

from .inbox import Inbox

class Me(object):
    
    def __init__(self, token):
        self.api = GraphAPI(oauth_token = token)

    def get_inbox(self):
        """
        Returns Inbox objects representing inbox of account
        """
        return Inbox(self.api.get("/me/inbox"))
