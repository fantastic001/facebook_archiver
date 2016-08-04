
from .. import Inbox 

import pyfacebook

class APIInbox(Inbox):
    
    def __init__(self, inbox):
        """
        Initializes inbox 

            :param inbox - dictionary which can be got from GraphAPI.get("/me/inbox")
        """
        self.inbox = pyfacebook.Inbox(inbox)

    def next(self): 
        """
        Returns Inbox object as next page. Facebook does not provide whole inbox at once and uses paging. 
        """
        return self.inbox.next()

    def prev(self): 
        """
        Returns Inbox object as previous page. Facebook does not provide whole inbox at once and uses paging. 
        """
        return self.inbox.prev()
    
    def has_next(self):
        return self.inbox.has_next()

    def has_prev(self):
        return self.inbox.has_prev()

    def get_conversations(self):
        """
        Returns list of Conversation objects 
        """
        return self.inbox.get_conversations()
