import requests
import json
import os

if 'RITO_SLACK_TOKEN' not in os.environ:
    print("To use Rito's slack functions, first create a Slack app on your workspace following these instructions: https://api.slack.com/messaging/sending#getting_started")
    print("Your app needs the permissions channel:read, chat:write, and chat:write.public")
    print("After creating the app and installing it to your workspace, copy its auth token into an environment variable called RITO_SLACK_TOKEN")
    exit(1)

auth_token = os.environ['RITO_SLACK_TOKEN']

# Instead of a string containing a message, the slack_image sender expects a string containing an image filename
def send_message(channel, filename):
    payload = {
        "channels": channel
    }

    headers = {
        "Authorization": "Bearer {}".format(auth_token)
    }

    files = {
        'file': open(filename, 'rb')
    }

    resp = requests.post("https://slack.com/api/files.upload", data=payload, headers=headers, files=files)
    resp = json.loads(resp.text)
    if not resp["ok"]:
        raise Exception(resp["error"])