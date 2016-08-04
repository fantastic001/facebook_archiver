
class Inbox(object):
    
    def __init__(self, inbox):
        """
        Initializes inbox 

            :param api - object of GraphAPI class 
            :param inbox - dictionary which can be got from GraphAPI.get("/me/inbox")
        """
        pass

    def next(self): 
        """
        Returns Inbox object as next page. Facebook does not provide whole inbox at once and uses paging. 
        """
        pass

    def prev(self): 
        """
        Returns Inbox object as previous page. Facebook does not provide whole inbox at once and uses paging. 
        """
        pass
    
    def has_next(self):
        pass

    def has_prev(self):
        pass

    def get_conversations(self):
        """
        Returns list of Conversation objects 
        """
        pass
