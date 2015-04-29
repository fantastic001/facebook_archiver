
from .exporter import * 

class TextExporter(Exporter):
    def on_start(self):
        return ""

    def on_end(self):
        return ""

    def on_message(self, message):
        return message.get_time().strftime("%Y %m %d %H:%M ") + message.get_sender() + ": " + message.get_message() + "\n"
