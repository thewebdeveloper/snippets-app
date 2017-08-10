import logging, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippetsDB.log", level=logging.DEBUG)

# Connect to the database from Python
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established")

def put(name, snippet):
	""" Store a snippet with associated name."""
	logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
	# cursor as a context manager
	with connection, connection.cursor() as cursor:
		try:
			cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
		except psycopg2.IntegrityError as e:
			connection.rollback()
			cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
			
	logging.debug("Snippet stored successfully...")
	return name, snippet
	
def get(name):
	"""
	Retrieve the snippet with a given name
	if the snippet is not existed, return '404: Snippets not found'
	Return the snippet
	"""
	logging.info("Retrieving snippet {!r}".format(name))
	# cursor as a context manager
	with connection, connection.cursor() as cursor:
		cursor.execute("select message from snippets where keyword=%s", (name,))
		row = cursor.fetchone()
	
	logging.debug("Snippet retrieved successfully...")
	if not row:
		# No snippet was found with that name.
		return "404: Snippet Not Found"
	return row
	
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