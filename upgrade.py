# coding=utf-8
import httplib,urllib,re, time, ssl , sys
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def help():
	print 'upgrade <Destination IP> <port> <username> <password> <http,https>'
	print 'example:'
	print 'upgrade 1.1.1.1 443 root password https'
	print 'upgrade 1.1.1.1 80 root password http'
	sys.exit()


if len(sys.argv) < 6:
	help()
host = sys.argv[1]
port = sys.argv[2]
user = sys.argv[3]
Pass = sys.argv[4]
prot = sys.argv[5]

#連線前準備，GW位置
# host = '10.10.1.223'
# user = 'octtel'
# Pass = '12841302'
#排除網站阻擋
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = { 'User-Agent' : user_agent}
#連線控制與URL


def http_get(prot,url):
	#列出來源頁面
	if prot == 'http':
		http_connect = httplib.HTTPConnection(host, port, timeout=10)	
	elif prot == 'https':
		http_connect = httplib.HTTPSConnection(host, port, timeout=10, context=ctx)	 	
	else:
		help()
	#print "<br>"
	#request(method, url, headers)
	#print (url,headers)
	http_connect.request('GET', url, '', headers)	
	#準備收取內容
	http_data = http_connect.getresponse()
	#Read page source html
	data = http_data.read()
	http_connect.close()
	#print data
	return data
	
	
def http_post(prot,url,params):
	#列出來源頁面
	if prot == 'http':
		http_connect = httplib.HTTPConnection(host, port, timeout=10)	
	elif prot == 'https':
		http_connect = httplib.HTTPSConnection(host, port, timeout=10, context=ctx)	 	
	else:
		help()
	#print "<br>"
	#request(method, url, body, headers)
	#print (host,url,params,headers)	
	# http_data = urllib.urlopen(url, params)
	http_connect.request('POST', url, params, headers)	
	# 準備收取內容
	http_data = http_connect.getresponse()
	# Read page source html
	data = http_data.read()
	http_connect.close()
	#print data	
	return data
	

systeminformation_url = '/goform/StatusLoad'
systeminformation = 'FORM=SystemInformationForm'
data = '123'

# login
def login():
	login_url = '/goform/LoginForm'
	login_pass = 'username='+user+'&password='+Pass
	url = "/LoginForm.asp"
	useless1 = http_get(prot,url)
	url = login_url
	params = login_pass
	login_page = http_post(prot,url,params)
	# print 'Login...'
	time.sleep(1)
	url = "/LoginFirstPageForm.asp"
	useless2 = http_get(prot,url)

# get status MAC, HW, Driver, Firmware
def status():
	url = '/goform/StatusLoad'
	params = 'FORM=SystemInformationForm'
	getinformation = http_post(prot,url,params)
	# print "-----------------------------------"
	# print getinformation
	# print "-----------------------------------"
	# str.find(str, beg=0, end=len(string))
	mac_head = getinformation.find('"WanMac":"')
	mac_tail = getinformation.find('"',mac_head+len('"WanMac":"'))
	mac = getinformation[mac_head+len('"WanMac":"'):mac_tail]
	# print mac
	firmware_head = getinformation.find('Ver(')
	firmware_tail = getinformation.find('==',firmware_head+len('Ver('))
	firmware_long = getinformation[firmware_head+len('Ver('):firmware_tail]	
	# print firmware_long
	firmware_tail = getinformation.find(' ',firmware_head+len('Ver('))
	firmware_short = getinformation[firmware_head+len('Ver('):firmware_tail]
	# print firmware_short
	return mac, firmware_long, firmware_short


# UI command firmware upgrade with tftp server
def upgrade():
	url = '/goform/UpgradeForm'
	params = 'K643_0=0&K122_0=10.10.1.123&K123_0=69&K645_0=&K646_0=&K124_0=&K638_0=0'
	upgrade_params = http_post(prot,url,params)
	url = '/goform/UpgradeLoadForm'
	params = 'FORM=UpgradeurlForm&IS_UPGRADE=UPGRADE&UPGRADE_MODE='
	upgrade_page = http_post(prot,url,params)
	# print upgrade_page

# save
def save():
	save_url = '/goform/RestartForm'
	save_params = 'FORM_INDEX=0&K48_0=1'
	url = save_url
	params = save_params
	save_page = http_post(prot,url,params)
	time.sleep(1)
	
# restart	
def restart():
	restart_url = '/goform/ConfigBackupLoadForm'
	restart_params = 'FORM_INDEX=0&K20_0=1&Config=ID_Reboot'
	url = restart_url
	params = restart_params
	restart_page = http_post(prot,url,params)
	url = '/goform/ConfigBackupLoadForm'
	params = "Config=ID_CallReboot"
	restart_page = http_post(prot,url,params)
	print "<br>"
	time.sleep(60)

# factory default and save
def factory():
	factory_url = '/goform/ConfigBackupLoadForm'
	factory_params = 'Config=ID_DefaultSetting'
	url = factory_url
	params = factory_params
	factory_page = http_post(prot,url,params)

login()
# get status MAC, HW, Driver, Firmware
mac, firmware_long, firmware_short = status()
print host, mac, firmware_long
# UI command firmware upgrade with tftp server
upgrade()
# Wait upgrade finish
# time.sleep(45)
login()
# Double check firmware version
mac, firmware_long, firmware_short = status()
# compare upgrade result
# Inform result

# factory default and save	
factory()
save()

# Ring 1 FXS
