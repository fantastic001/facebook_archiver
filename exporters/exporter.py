
class Exporter(object):
    """
    Basic abstract exporter for using as base class for specific exporters 
    """
    
    def __init__(self, filename):
        self.f = open(filename, "w")
        self.f.write(self.on_start())

    def finish(self):
        self.f.write(self.on_end())
        self.f.close()

    def print_message(self, message):
        """
        Method for printing messages, uses Exporter.onMessage method 
        """
        self.f.write(self.on_message(message))

    def on_start(self):
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
        Should return a string for printing
        """
        pass
