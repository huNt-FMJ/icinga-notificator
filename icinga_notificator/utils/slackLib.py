#!/usr/bin/env/python3
#
# Slack message sending lib
#

# compatibility removed (py2)

import logging
import urllib
import urllib.parse
import urllib.request
import json
import ssl

# import slackclient
# Sending function - using Slack Api
# need to provide token, username of user (will look for id)

# due to the older python version there is workaround via urllib..


def sendSlackMessage(token, username, message):

    channel = None

    # Load users and find the correct ID
    try:
        getUsersUrl = "https://slack.com/api/users.list"
        args = {"token": token}
        encodedArgs = urllib.parse.urlencode(args)
        url = getUsersUrl + "?" + encodedArgs
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception:
        logging.exception("Something bad happened while trying to contact slack API")
        raise Exception("Error when trying to contact API")

    if result["ok"] is not True:
        raise Exception("Error in API communication")

    for member in result["members"]:
        if member["name"] == username:
            channel = member["id"]

    if channel == None:
        raise Exception("Slack user not found, cannot send message")

    # Send message to user
    try:
        getUsersUrl = "https://slack.com/api/chat.postMessage"
        args = {"token": token, "text": message, "channel": channel, "as_user": "true"}
        encodedArgs = urllib.parse.urlencode(args)
        url = getUsersUrl + "?" + encodedArgs
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception:
        logging.exception("Something bad happened while trying to contact slack API")
        raise Exception("Error when trying to contact API")

    if result["ok"] is not True:
        raise Exception("Error in API communication")

    return 0
