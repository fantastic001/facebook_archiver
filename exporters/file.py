
from .exporter import * 

class FileExporter(Exporter):
    """
    Basic abstract file exporter for using as base class for specific exporters that write directly to files
    """
    
    def on_start(self, **params):
        self.f = open(params.get("filename", "messages.txt"), "w")

    def on_end(self):
        self.f.close()

    def on_message(self, message):
        self.f.write(self.print_message(message))

    def print_message(self, message):
        """
        Implement, put format of message here 
        """
        return ""
