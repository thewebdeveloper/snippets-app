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
	
	
def catalog():
	""" Retrieve all the the keywords in snippets """
	logging.info("Retrieving keywords in snippets")
	# cursor as a context manager
	with connection, connection.cursor() as cursor:
		cursor.execute("select keyword from snippets order by keyword")
		rows = cursor.fetchall()
		for row in rows:
			print (row)
			
	logging.debug("keywords retrieved successfully...")
	return row
	
	
def search(name):
	""" Search for the name of the keyword in the snippets database """
	logging.info("Searching the keyword {!r} in the snippets database".format(name))
	
	with connection, connection.cursor() as cursor:
		cursor.execute("select keyword from snippets where keyword LIKE '%" + name + "%'")
		rows = cursor.fetchall()
			
	logging.debug("The searched keyword retrieved successfully...")
	if not rows:
		return "No Keyword matched your search"
	return rows
	
	
def delete(name):
	""" Delete the whole record based on the keyword """
	logging.info("Deleting the keyword {!r} with its description".format(name))
	
	with connection, connection.cursor() as cursor:
		cursor.execute("delete from snippets where keyword=%s", (name,))
	
	if cursor.rowcount < 1:
		return "No Keyword with {} found".format(name)
	return "Total number of rows deleted :", cursor.rowcount
	
	
def main():
	"""The Main Function"""
	logging.info("Constructing Parser")
	parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
	
	# Add subparsers
	subparsers = parser.add_subparsers(dest="commands", help="Available commands")
	
	
	# Subparser for listing all the keywords in snippets database
	logging.debug("Listing all keywords")
	subparsers.add_parser(None, help="List all keywords in snippets")
	
	# Subparser for the Search command
	logging.debug("Constructing search subparser")
	search_parser = subparsers.add_parser("search", help="Search a keyword")
	search_parser.add_argument("name", help="Name of the Keyword being searhed for")
	
	# Subparser for the Put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help="Store a snippet")
	put_parser.add_argument("name", help="Name of the snippet")
	put_parser.add_argument("snippet", help="Snippet text")
	
	# Subparser for the Get command
	logging.debug("Constructing get subparser")
	get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
	get_parser.add_argument("name", help="Name of the snippet")
	
	# Subparser for the Delete command
	logging.debug("Constructing delete subparser")
	delete_parser = subparsers.add_parser("delete", help="Delete a snippet")
	delete_parser.add_argument("name", help="Name of the snippet")
	
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
	elif command == "search":
		name = search(**arguments)
		print("Retrieved the searched keyword:\n {!r}".format(name))
	elif command == "delete":
		name = delete(**arguments)
		print("{!r}".format(name))
	elif command == None:
		print("The list of the keywords available in Snippets Database\n")
		snippet = catalog()
	
	
if __name__ == "__main__":
	main()