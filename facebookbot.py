import requests
import json

ACCESS_TOKEN="" # Put your facebook access token here
FLY_GROUP = "1901609943449329"

def post_to_group(content, grid=FLY_GROUP):
	url = "https://graph.facebook.com/%s/comments?access_token=%s" % (grid, ACCESS_TOKEN)
	data = {"message" : content, "access_token" : ACCESS_TOKEN}
	res = requests.post(url, data=data)
	data = json.loads(res.text)
	print(data)
