
from bs4 import BeautifulSoup, NavigableString
import argparse

from exporters import * 

from datetime import datetime
import re
from datetime import datetime


class Message(object):
    

    def __init__(self, user, time_str):
        self.user = user
        #self.time = datetime.strptime(self.pre_format(time_str), '%A, %B %d, %Y at %I:%M%p %Z%z')
        self.time = self.pre_format(time_str)
        self.content = ""
    
    def pre_format(self, time_str):
        r = re.compile(r"^(\w+), (\w+) (\d+), (\d+) at (\d+):(\d+)(\w+) (\w+)")
        m = r.match(time_str)
        if m:
            months = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }
            return datetime(int(m.group(4)), months[m.group(2)], int(m.group(3)), int(m.group(5)), int(m.group(6)))

    def add_content(self, text):
        self.content += text

    def get_sender(self):
        return self.user

    def get_message(self):
        return self.content

    def get_time(self):
        return self.time


class ArchiveParser(object):
    
    def __init__(self, source):
        self.source = source
        f = open("%s/html/messages.htm" % self.source, "r")
        self.doc = f.read()
        f.close()
        self.soup = soup = BeautifulSoup(self.doc, 'html.parser')
        self.threads = self.soup.find_all(class_="thread")

    def get_list(self):
        res = []    
        for thread in self.threads:
            for child in thread.children:
                res.append(child)
                break
        return res

    def get_candidates(self, person):
        """
        Returns list of candidates.

        Every element is a dictionary with 'thread' and 'name' fields.
        """
        candidates = []
        for thread in self.threads:
            name = ""
            for child in thread.children:
                name = child
                break
            if person in name:
                candidates.append({"thread": thread, "name": name})
        return candidates

    def export_messages(self, target, exporter):
        """
        target: thread from candidates, it can be accessed as candidates[i]['thread']
        """
        messages = []
        for c in target.contents:
            if not isinstance(c, NavigableString) and "class" in c.attrs.keys() and "message" in c["class"]:
                messages.append(Message(c.find(class_="user").text, c.find(class_="meta").text))
            else:
                if len(messages) > 0:
                    messages[-1].add_content(c.text)
        for m in messages[::-1]:
            exporter.on_message(m)
        exporter.finish()


parser = argparse.ArgumentParser(description='Facebook archive reader.')

parser.add_argument("--source", help="Directory where archive is held")
parser.add_argument("--person", help="Person name for processing")
parser.add_argument("--output", help="Output file for storing messages to")
parser.add_argument("--action", choices=["log", "list"], required=True, help="Action to take")
parser.add_argument("--export", choices=["text", "latex"], default="text", help="Select export format")
#parser.add_argument("--after",
#                    help="Specify date which is last considered date, format is e.g. 2015-01-01T00:00:00+0000",
#                    required=False
#                    )
args = parser.parse_args()
action = args.action

parser = ArchiveParser(args.source)

if action == "list":
    l = parser.get_list()
    for ll in l:
        print(ll)
elif action == "log":
    person = args.person
    output = args.output
    exporters = {
        "latex": LatexExporter,
        "text": TextExporter
    }
    exporter = exporters[args.export](filename=output)
    print("Collecting candidates...")
    candidates = parser.get_candidates(person)
    target = None
    if len(candidates) == 0:
        print("Person not found")
        exit(1)
    elif len(candidates) > 1:
        print("You have multiple candidates, select one of them")
        i = 0
        for c in candidates:
            print("%d: %s" % (i+1, c["name"]))
            i += 1
        choice = input(">>> ")
        target = candidates[int(choice)-1]["thread"]
    else:
        target = candidates[0]["thread"]
    print("Exporting messages...")
    parser.export_messages(target, exporter)

