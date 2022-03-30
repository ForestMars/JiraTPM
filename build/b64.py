import base64
import sys
from pprint import pprint


string2encode = "justincodes32@gmail.com:dRQvshnC4lgKiQTLtLaj3C4C"
string_bytes = string2encode.encode("ascii")

base64_bytes = base64.b64encode(string_bytes)
base64_string = base64_bytes.decode("ascii")

print(f"Encoded string: {base64_string}")
# anVzdGluY29kZXMzMkBnbWFpbC5jb206ZFJRdnNobkM0bGdLaVFUTHRMYWozQzRD

r = {"self":"https://justincodes.atlassian.net/rest/api/3/project/search?maxResults=50&startAt=0","maxResults":50,"startAt":0,"total":1,"isLast":True,"values":[{"expand":"description,lead,issueTypes,url,projectKeys,permissions,insight","self":"https://justincodes.atlassian.net/rest/api/3/project/10000","id":"10000","key":"TES","name":"test1","avatarUrls":{"48x48":"https://justincodes.atlassian.net/rest/api/3/universal_avatar/view/type/project/avatar/10403","24x24":"https://justincodes.atlassian.net/rest/api/3/universal_avatar/view/type/project/avatar/10403?size=small","16x16":"https://justincodes.atlassian.net/rest/api/3/universal_avatar/view/type/project/avatar/10403?size=xsmall","32x32":"https://justincodes.atlassian.net/rest/api/3/universal_avatar/view/type/project/avatar/10403?size=medium"},"projectTypeKey":"software","simplified":True,"style":"next-gen","isPrivate":False,"properties":{},"entityId":"cc399cd7-6da2-4efa-888b-0ae1df73c39b","uuid":"cc399cd7-6da2-4efa-888b-0ae1df73c39b"}]}

pprint(r)

sys.exit()

"""
curl --request GET \
  --url 'https://justincodes.atlassian.net/rest/api/3/project/search' \
  --header 'Authorization: Basic anVzdGluY29kZXMzMkBnbWFpbC5jb206ZFJRdnNobkM0bGdLaVFUTHRMYWozQzRD' \
  --header 'Accept: application/json'
"""
