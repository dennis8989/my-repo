import requests

url ='http://https://www.ptt.cc/bbs/Gossiping/index.html/'
#
res = requests.get(url)
res.status_code
# print(res)