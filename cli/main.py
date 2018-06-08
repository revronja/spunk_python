
import requests
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

passw = input("enter password")

url = "https://10.0.0.62:8089/services/auth/login"
data = {"username":"Admin",
"password":str(passw)}
r = requests.post(url, data=data, verify=False)

if r.ok:
   root = ET.fromstring(r.content)
   myElement = root.find('sessionKey')
   authToken = myElement.text
else:
   print("error")

url = "https://10.0.0.62:8089/services/search/jobs"
auth_str = "Splunk {}".format(authToken)
headers = { "Authorization": auth_str}
payload = {
"search":"buttercupgames(error OR fail * OR severe"
        }
r = requests.post(url, headers=headers, params=payload, verify=False)

root = ET.fromstring(r.content)
# response has "sid" in there
for child in root.iter('*'):
    print(child.text)
    #print(child.tag, child.attrib)
