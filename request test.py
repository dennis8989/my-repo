import requests
payload = {
'from': '/bbs/Gossiping/index.html',
'yes': 'yes'
}
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html')
print(res.text)