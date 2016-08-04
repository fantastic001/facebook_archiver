
class Conversation(object):
    
    def __init__(self, data, comments=None):
        """
        Initializes new Conversation object 

            :param data - dictionary data which can be got from inbox data field 
            :param comments - provide separate comments
        """
        pass

    def get_persons(self):
        """
        Returns list of strings which represents persons being chated with 
        """
        pass

    def get_messages(self):
        """
        Returns list of Message objects which represents messages being transported.
        """
        pass

    def next(self):
        """
        Returns next paging
        """
        pass

    def prev(self):
        """
        Returns previous paging
        """
        pass
