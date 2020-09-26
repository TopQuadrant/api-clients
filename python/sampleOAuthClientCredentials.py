#!/usr/bin/python
#
"""
Sample API client using OAuth 2 client credentials flow.  It will will repeat
an API call every hour and generate a new token as needed.

1. Call API
2. If access token is expired, use the client_secret to get a new one
3. Repeat

@author: TopQuadrant
"""
import getpass
import json
import time
import urllib
import urllib2

def authenticate(url, client_id):
    """
    Authenticates the client and generates a new access token.
    """
    client_secret = getpass.getpass("Client secret: ")
    request_data = { 
        "client_id" : client_id,
        "client_secret" : client_secret,
        "grant_type" : "client_credentials"
    }
    encoded_data = urllib.urlencode(request_data)
    request = urllib2.Request(url, encoded_data)
    print("Getting token...")
    response = urllib2.urlopen(request)
    # Just to be safe...
    client_secret = None
    tokens = json.load(response)
    access_token = tokens["access_token"]
    return access_token

# Copy your authorization server URL and paste it here
auth_server_url = "https://your.adfs.server/adfs/oauth2/token"
# Copy your client ID and paste it here
client_id = "12345678-90ab-cdef-1234-567890abcdef"
# Copy your EDG API URL and paste it here
api_url = "https://your.edg.server/edg/tbl/sparql"
# Copy your initial access_token you got from the authorization server and paste it here
access_token = ""

# Run the API call once per hour
print("Running hourly process...")
while True:
    # What time is it?
    print(time.strftime("%c"))
    # Use the access token
    auth_header = { "Authorization" : "Bearer " + access_token }
    # Make a request
    request = urllib2.Request(api_url, None, auth_header)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as error:
        # Check status code
        if error.code == 401:
            # Need to use client_secret to get a new token
            access_token = authenticate(auth_server_url, client_id)
            # Use the new access token
            auth_header = { "Authorization" : "Bearer " + access_token }
            # Repeat the request
            request = urllib2.Request(api_url, None, auth_header)
            # Get the response
            response = urllib2.urlopen(request)
    print("Response status was " + str(response.getcode()))
    # Do something useful with the response.  (Your biz logic goes here)
    # result = json.load(response)
    # 
    # Wait until next time
    print("Sleeping.")
    time.sleep(3600)


