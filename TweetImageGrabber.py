import sys
import subprocess
import google

try:
	from google import search
except ImportError: 
	print("No module named 'google' found")
 
# to search
query = sys.argv[0]
 
j = google.search(query, tld="co.in", num=10, stop=1, pause=2)

print(j)