
from .. import Me 
import pyfacebook

class APIMe(Me):
    
    def __init__(self, token):
        self.me = pyfacebook.Me(token)

    def get_inbox(self):
        """
        Returns Inbox objects representing inbox of account
        """
        return self.me.get_inbox()

    def get_token_uri(APP_ID, scope):
        """
        Returns URL for getting tokens 
        """
        return self.me.get_token_uri(APP_ID, scope)
