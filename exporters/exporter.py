
class Exporter(object):
    """
    Basic abstract exporter for using as base class for specific exporters 
    """
    
    def __init__(self, **params):
        self.on_start(**params)
    
    def finish(self):
        self.on_end()

    def on_start(self, **params):
        """
        Called when exporter is made
        """
        pass

    def on_end(self):
        """
        Called on the end of export process
        """
        pass

    def on_message(self, message):
        """
        Called when processing specific message
        """
        pass
