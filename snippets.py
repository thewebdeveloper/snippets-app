import logging, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
	"""
	Store a snippet with associated name
	Return the snippet and the name
	"""
	logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
	return name, snippet
	
def get(name):
	"""
	Retrieve the snippet with a given name
	if the snippet is not existed, return '404: Snippets not found'
	Return the snippet
	"""
	logging.error("FIXME: Unimplemented - get({!r})".format(name))
	return ""
	
def main():
	"""The Main Function"""
	logging.info("Constructing Parser")
	parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
	
	# Add subparsers
	subparsers = parser.add_subparsers(dest="commands", help="Available commands")
	
	# Subparser for the Put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help="Store a snippet")
	put_parser.add_argument("name", help="Name of the snippet")
	put_parser.add_argument("snippet", help="Snippet text")
	
	# Subparser for the Get command
	logging.debug("Constructing get subparser")
	get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
	get_parser.add_argument("name", help="Name of the snippet")
	
	arguments = parser.parse_args()
	
	# Convert parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	# removes the command in the dictionary, and saves it variable 'command'
	command = arguments.pop("commands")
	
	if command == "put":
		name, snippet = put(**arguments)
		print("Stored {!r} as {!r}".format(name, snippet))
	elif command == "get":
		snippet = get(**arguments)
		print("Retrieved snippet: {!r}".format(snippet))
	
	
if __name__ == "__main__":
	main()