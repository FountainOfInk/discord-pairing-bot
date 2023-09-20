import requests
import json

token = "MTEwNTcxMTYwMjE5NzYxMDQ5Ng.G8N_1z.IfBjxXZhgFRbgoZB_w6RtFcc9bbPugjzZTHSa0"
base = "https://canary.discord.com/api"

verb = "GET"
endpoint = "/guilds/1105251085549051974/channels"

headers = {
    "Authorization": f"Bot {token}"
}

payload = None
def request(verb: str, endpoint: str, **kwargs):
    return requests.request(verb, base+endpoint, headers=headers, **kwargs)
# payload = {
#     "content": "hi!!"
# }

# if payload:
#     src = requests.request(verb, base + endpoint, headers=headers, json=payload)
# else:
#     src = requests.request(verb, base + endpoint, headers=headers)

chans = []
channel_types = {
    0: "Text",
    1: "DM",
    2: "Voice",
    3: "Group DM",
    4: "Category",
}

guild_id = "1105251085549051974"
src = requests.get(base + endpoint, headers=headers)
i = 0
for channel in src.json():
    print(f"{i}. {channel_types[channel['type']]} Channel: {channel['name']}: {channel['id']}")
    chans.append(channel)
    i += 1

selected_channel = chans[int(input("Select a channel: "))]
print(f"\nShowing messages for channel `{selected_channel['name']}`:")
for message in request("GET", f"/channels/{selected_channel['id']}/messages").json():
    print("    " + f"{message['author']['username']}: {message['content']}")