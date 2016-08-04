
from .. import Message 
import pyfacebook 

class APIMessage(Message):
    
    def __init__(self, data, conversation):
        self.message = pyfacebook.Message(data, conversation)

    def get_sender(self):
        """
        Returns string representing sender name
        """
        return self.message.get_sender()

    def get_message(self):
        return self.message.get_message()

    def __str__(self):
        return str(self.message)

    def get_time(self):
        return self.message.get_time()

    def __eq__(self, msg):
        return msg == self.message
