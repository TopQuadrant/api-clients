#!/usr/local/bin/python3
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
import urllib.parse
import urllib.request
import ssl

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
    encoded_data = urllib.parse.urlencode(request_data)
    binary_data = encoded_data.encode('ascii')
    request = urllib.request.Request(url)
    print("Getting token...")
    response = urllib.request.urlopen(request, binary_data)
    # Just to be safe...
    client_secret = None
    tokens = json.load(response)
    access_token = tokens["access_token"]
    return access_token

# Copy your authorization server URL and paste it here
auth_server_url = "https://your.okta.com/oauth2/default/v1/token"
# Copy your client ID and paste it here
client_id = "0123456789abcdefghij"
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
    request = urllib.request.Request(api_url, None, auth_header)
    try:
        response = urllib.request.urlopen(request)
        print("Response status was " + str(response.getcode()))
    except urllib.error.HTTPError as error:
        # Check status code
        if error.code == 401:
            # Need to use client_secret to get a new token
            access_token = authenticate(auth_server_url, client_id)
            # Use the new access token
            auth_header = { "Authorization" : "Bearer " + access_token }
            # Repeat the request
            request = urllib.request.Request(api_url, None, auth_header)
            # Get the response
            response = urllib.request.urlopen(request)
            print("Response status was " + str(response.getcode()))
    # Do something useful with the response.  (Your biz logic goes here)
    # result = json.load(response)
    # 
    # Wait until next time
    print("Sleeping.")
    time.sleep(3600)


