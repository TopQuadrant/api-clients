#!/usr/bin/python
#
"""
Sample API client using OAuth 2 authorization code flow.  It will will repeat
an API call every hour and refresh the tokens as needed.

1. Call API
2. If access token is expired, use the refresh token to get a new one
3. Repeat

@author: TopQuadrant
"""
import json
import time
import urllib
import urllib2

def refresh_tokens(url, client_id, refresh_token):
    """
    Uses the refresh token to request new tokens from the authorization server.
    """
    request_data = { 
        "client_id" : client_id,
        "refresh_token" : refresh_token,
        "grant_type" : "refresh_token"
    }
    encoded_data = urllib.urlencode(request_data)
    request = urllib2.Request(url, encoded_data)
    print("Refreshing access token...")
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as error:
        # Something went wrong...
        print(error.reason)
        print("Perhaps your refresh token has expired.")
        return None, None
    tokens = json.load(response)
    access_token = tokens["access_token"]
    try:
        new_refresh_token = tokens["refresh_token"]
    except KeyError as error:
        print("Did not get a new refresh token...")
        new_refresh_token = refresh_token
    if new_refresh_token != refresh_token:
        print("Refreshed the refresh token...")
    return access_token, new_refresh_token

# Copy your authorization server URL and paste it here
auth_server_url = "https://your.adfs.server/adfs/oauth2/token"
# Copy your client ID and paste it here
client_id = "12345678-90ab-cdef-1234-567890abcdef"
# Copy your EDG API URL and paste it here
api_url = "https://your.edg.server/edg/tbl/sparql"
# Copy your initial access_token you got from the authorization server and paste it here
access_token = ""
# Copy your initial refresh_token you got from the authorization server and paste it here
refresh_token = ""

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
            # Need to use refresh token to get new token(s)
            access_token, refresh_token = refresh_tokens(auth_server_url, client_id, refresh_token)
            if access_token and refresh_token:
                # Use the new access token
                auth_header = { "Authorization" : "Bearer " + access_token }
                # Repeat the request
                request = urllib2.Request(api_url, None, auth_header)
                # Get the response
                response = urllib2.urlopen(request)
            else:
                print("Unable to refresh tokens, exiting.")
                break
    print("Response status was " + str(response.getcode()))
    # Do something useful with the response.  (Your biz logic goes here)
    # result = json.load(response)
    # 
    # Wait until next time
    print("Sleeping.")
    time.sleep(3600)


