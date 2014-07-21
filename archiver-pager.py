
import facebook 
import sys
import time


if sys.argv[1] in ["help", "--help", "-h", "-help"]:
	print """Usage: 
	archiver token log personid outputfile		Output whole log into file 
	archiver token show-conversations		Show all conversations and person ids 
"""

token = sys.argv[1] 
action = sys.argv[2]

if not action in ["log", "show-conversations"]:
	print "Wrong option. Use archiver --help for more information"


g = facebook.GraphAPI(token) 

# show-conversations option 
if action == "show-conversations": 	
	inbox = g.get_connections("me", "inbox", limit=5000) 
	for conversation in inbox["data"]: 
		to = conversation["to"]["data"] 
		for i in to: 
			print i["name"] + "(" + i["id"] + ")",
		print
	exit(0)


# log option
person = sys.argv[3] 
output_filename = sys.argv[4]

class Message(object): 
	"""
	Represents a one message in facebook chat 
	"""

	def __init__(self, data): 
		"""
		Initializes object with given data (dictionary with ids of persons, message, creating time etc) 
		
		data: dict
		"""
		self.date_string = data["created_time"].split("T")[0]
		self.time_string = data["created_time"].split("T")[1]
		self.message = data.get("message")
		if self.message == None: 
			self.message = ""
		self.sender = data["from"]["name"] 

def get_next_page(conversation): 
	"""
	Returns a new conversation (comments) dictionary with new (next) page 

	conversation: starting page 

	returns: next page
	"""
	next_url = conversation["paging"]["next"]
	res = facebook.requests.request("GET", next_url).json()
	while "error" in res.keys() and res["error"]["code"] == 613: 
		print "Delaying..." 
		time.sleep(180)
		res = facebook.requests.request("GET", next_url).json()
	return res

def get_prev_page(conversation): 
	"""
	Returns a new conversation (comments) dictionary with new (prev) page 

	conversation: starting page 

	returns: previous page
	"""
	next_url = conversation["paging"]["previous"]
	res = facebook.requests.request("GET", next_url).json()
	while "error" in res.keys() and res["error"]["code"] == 613: 
		print "Delaying..." 
		time.sleep(180)
		res = facebook.requests.request("GET", next_url).json()
	return res

def get_messages(conversation): 
	"""
	Get messages from conversation 

	conversation: dict object which represents "comments" dictionary in the actual facebook json representation 

	returns: list of Message objects 
	"""
	messages = [] 
	for m in conversation["data"]:
		messages.append(Message(m))
	return messages

inbox = g.get_connections("me", "inbox", limit=5000) 

target = None

for conversation in inbox["data"]: 
	to = conversation["to"]["data"] 
	for i in to: 
		if i["id"] == person or i["name"] == person: 
			print i["name"] +  " found"
			target = conversation 


conversation = target["comments"] 
new = conversation 
print "Getting prev pages"

start = time.time()

msgs = [] 

while "paging" in new.keys():
	conversation = new
	new = get_next_page(new)
	page = get_messages(conversation)
	msgs = page + msgs
	print msgs[0].date_string
 

print "Transfered to start in " + str(time.time() - start ) + " seconds" 
print "Collecting messages" 

time.sleep(10)

start = time.time()

#while "paging" in conversation.keys():
#	msgs.extend(get_messages(conversation)) 
#	print conversation
#	conversation = get_prev_page(conversation) 

output = open(output_filename, "w")

for m in msgs: 
	output.write(m.date_string.encode("UTF-8") + " " + m.time_string.encode("UTF-8") + " " + m.sender.encode("UTF-8") + "\t" + m.message.encode("UTF-8") + "\n")

print "Processed " + str(len(msgs)) + " in " + str(time.time() - start) + " seconds"
