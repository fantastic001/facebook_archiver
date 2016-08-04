
import pyfacebook

from .. import Conversation

class APIConversation(Conversation):
    
    def __init__(self, data, comments=None):
        """
        Initializes new Conversation object 

            :param data - dictionary data which can be got from inbox data field 
            :param comments - provide separate comments
        """
        self.conversation = pyfacebook.Conversation(data, comments)

    def get_persons(self):
        """
        Returns list of strings which represents persons being chated with 
        """
        return self.conversation.get_persons()

    def get_messages(self):
        """
        Returns list of Message objects which represents messages being transported.
        """
        return self.conversation.get_messages()

    def next(self):
        """
        Returns next paging
        """
        return self.conversation.next()

    def prev(self):
        """
        Returns previous paging
        """
        return self.conversation.prev()
