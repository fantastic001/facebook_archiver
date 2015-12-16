
from .file import * 

class TextExporter(FileExporter):

    def print_message(self, message):
        return message.get_time().strftime("%Y %m %d %H:%M ") + message.get_sender() + ": " + message.get_message() + "\n"
