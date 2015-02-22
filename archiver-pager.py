
import sys
import time

from facebook.me import Me
from facebook.exceptions import LimitExceededException

if sys.argv[1] in ["help", "--help", "-h", "-help"]:
    print("""Usage: 
    archiver token log personid outputfile          Output whole log into file 
    archiver token show-conversations               Show all conversations and person ids 
""")
    exit(0)



token = sys.argv[1] 
action = sys.argv[2]

if not action in ["log", "show-conversations"]:
    print("Wrong option. Use archiver --help for more information")


me = Me(token)

# show-conversations option 
if action == "show-conversations":      
    inbox = me.get_inbox()
    while inbox.has_next():
        for conversation in inbox.get_conversations():
            print(conversation)
        inbox = inbox.next()

    exit(0)


# log option
person = sys.argv[3] 
output_filename = sys.argv[4]

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
