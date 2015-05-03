
from .exporter import * 

class LatexExporter(Exporter):
    def on_start(self):
        s = ""
        s += r"\documentclass{memoir}" + "\n"
        s += r"\usepackage[utf8]{inputenc}" + "\n"
        s += r"\usepackage[T1]{fontenc}" + "\n"
        s += r"\begin{document}" + "\n"
        #s += r"\title{Chat report: %s}" % ", ".join(self.conversation.get_persons()) # TODO Modify Exporter class to support Conversation objects as argument to this method
        #s += r"\author{Stefan Nožinić}"
        #s += r"\date{}"
        #s += r"\maketitle"
        s += r"\newpage" + "\n"

        s += r"\section{Messages}" + "\n"
        return s

    def on_end(self):
        s = ""
        s += "\n"
        s += "\end{document}"
        return s

    def on_message(self, message):
        s = r"%s - %s: %s " % (message.get_time().strftime("%Y %m %d %H:%M "), message.get_sender(), message.get_message()) 
        s += "\n\n\n"
        return s
