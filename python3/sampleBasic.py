#!/usr/local/bin/python3
#
"""
Sample API client using Basic Auth.  It will will repeat an API call every hour.

1. Call API
2. Repeat

@author: TopQuadrant
"""
import getpass
import json
import time
import base64
import urllib.parse
import urllib.request
import ssl

def authenticate(username):
    """
    Generates a Basic auth credential for username and password.
    """
    password = getpass.getpass("Password: ")
    credential = base64.b64encode(bytes(username + ":" + password, "utf-8")).decode("ascii")
    # Just to be safe...
    password = None
    return credential

# Copy your EDG API URL and paste it here
api_url = "https://your.edg.server/edg/tbl/sparql"

# Who are you?
username = input("Enter username: ")
# Get the credential
credential = authenticate(username)

# Run the API call once per hour
print("Running hourly process...")
while True:
    # What time is it?
    print(time.strftime("%c"))
    # Use the credential
    auth_header = { "Authorization" : "Basic " + credential }
    # Make a request
    request = urllib.request.Request(api_url, None, auth_header)
    response = None
    try:
        response = urllib.request.urlopen(request)
        print("Response status was " + str(response.getcode()))
    except urllib.error.HTTPError as error:
        # Check status code
        print("Response status was " + str(error.code))
    # Do something useful with the response.  (Your biz logic goes here)
    # result = json.load(response)
    # 
    # Wait until next time
    print("Sleeping.")
    time.sleep(3600)


