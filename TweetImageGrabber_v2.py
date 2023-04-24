import sys
from googlesearch import search


def search_google(query):
    # Search for the query and get the first result
    try:
        first_result = next(search(query, num_results=1, pause=2.0))
        print(first_result)
    except StopIteration:
        print(f"No results found for query '{query}'.")
    except Exception as e:
        print(f"Error occurred while searching for query '{query}': {e}.")


if __name__ == "__main__":
    # Get the query from command line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search_google(query)
    else:
        print("Please provide a query to search for as a command line argument.")
