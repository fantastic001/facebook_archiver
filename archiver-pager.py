
import sys
import time
import argparse

from template import *

from pyfacebook.me import Me
from pyfacebook.exceptions import LimitExceededException

from exporters import *

from datetime import datetime

def get_token():
    print("Go to %s" % Me.get_token_uri(APP_ID, "read_mailbox"))
    exit(0)

parser = argparse.ArgumentParser(description='Facebook message archiving tool.')

parser.add_argument("--token", help="Token for using while accessing facebook private data")
parser.add_argument("--person", help="Person name for processing")
parser.add_argument("--output", help="Output file for storing messages to")
parser.add_argument("--action", choices=["log", "list", "token"], required=True, help="Action to take")
parser.add_argument("--export", choices=["text", "latex"], default="text", help="Select export format")
parser.add_argument("--after",
                    help="Specify date which is last considered date, format is e.g. 2015-01-01T00:00:00+0000",
                    required=False
                    )
args = parser.parse_args()

exporter_labels = {
    "text": TextExporter,
    "latex": LatexExporter
}

token = args.token
action = args.action
after = None
if args.after != None:
    after = datetime.strptime(args.after, "%Y-%m-%dT%H:%M:%S%z")

me = Me(token)

if action == "token":
    get_token()

if action == "list":
    inbox = me.get_inbox()
    while inbox.has_next():
        for conversation in inbox.get_conversations():
            print(conversation)
        inbox = inbox.next()
    exit(0)


# log option
person = args.person
output_filename = args.output
print("Starting gathering information...")
inbox = me.get_inbox()

available_targets = []
while inbox.has_next():
    for conversation in inbox.get_conversations():
        if person in conversation.get_persons():
            available_targets.append(conversation)
    inbox = inbox.next()

target = None
if len(available_targets) > 1:
    print("You have multiple choices for target, select one of them by typing desired number:")
    i = 1
    for t in available_targets:
        print(str(i) + ": " + str(t))
        i += 1
    selection = int(input(">>> "))
    target = available_targets[selection - 1]
else:
    if len(available_targets)==0:
        print("Target not found")
        exit(1)
    else:
        target = available_targets[0]


start = time.time()

msgs = []
targets = []
while target.has_next():
    new_target = None
    try:
        new_target = target.next()
    except LimitExceededException:
        print("Delaying some time")
        time.sleep(100)
    else:
        target = new_target
        new_msgs = target.get_messages()
        if len(target.get_messages()) > 0:
            print("Got messages from " + str(new_msgs[0].get_time()))
        to_add = []
        if after != None:
            found_older = False
            for mmm in new_msgs:
                if mmm.get_time() > after:
                    to_add.append(mmm)
        else:
            to_add = new_msgs
        msgs = to_add + msgs
        if len(to_add) < len(new_msgs):
            break


print("Transfered to start in " + str(time.time() - start ) + " seconds")
print("Collecting messages")

time.sleep(10)

start = time.time()

#while "paging" in conversation.keys():
#       msgs.extend(get_messages(conversation))
#       print conversation
#       conversation = get_prev_page(conversation)

exporter = exporter_labels[args.export](filename=output_filename)
for msg in msgs:
    exporter.on_message(msg)
exporter.finish()

print("Processed " + str(len(msgs)) + " in " + str(time.time() - start) + " seconds")
