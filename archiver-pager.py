
import sys
import time
import argparse

from template import * 

from pyfacebook.me import Me
from pyfacebook.exceptions import LimitExceededException

def get_token():
    print("Go to %s" % Me.get_token_uri(APP_ID, "read_mailbox"))
    exit(0)

parser = argparse.ArgumentParser(description='Facebook message archiving tool.')

parser.add_argument("--token", help="Token for using while accessing facebook private data")
parser.add_argument("--person", help="Person name for processing")
parser.add_argument("--output", help="Output file for storing messages to")
parser.add_argument("--action", choices=["log", "list", "token"], required=True, help="Action to take")

args = parser.parse_args()

token = args.token
action = args.action

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
        msgs = new_msgs + msgs
 

print("Transfered to start in " + str(time.time() - start ) + " seconds") 
print("Collecting messages") 

time.sleep(10)

start = time.time()

#while "paging" in conversation.keys():
#       msgs.extend(get_messages(conversation)) 
#       print conversation
#       conversation = get_prev_page(conversation) 

output = open(output_filename, "w")

for msg in msgs:
    output.write(msg.get_time().strftime("%Y %m %d %H:%M ") + msg.get_sender() + ": " + msg.get_message() + "\n")

print("Processed " + str(len(msgs)) + " in " + str(time.time() - start) + " seconds")
