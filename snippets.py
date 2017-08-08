import logging, argparse

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
	arguments = parser.parse_args()
	
	
if __name__ == "__main__":
	main()