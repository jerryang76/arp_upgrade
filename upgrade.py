# coding=utf-8
import httplib,urllib,re, time, ssl , sys, os, subprocess, platform
from sys import executable
from subprocess import Popen

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def help():
	print 'upgrade <Destination IP> <port> <username> <password> <http,https> <build_number>'
	print 'example:'
	print 'upgrade 1.1.1.1 443 username password https 3055'
	print 'upgrade 1.1.1.1 80 username password http 3055'
	os.system("pause")
	sys.exit()


if len(sys.argv) < 7:
	help()
host = sys.argv[1]
port = sys.argv[2]
user = sys.argv[3]
Pass = sys.argv[4]
prot = sys.argv[5]
build_check = sys.argv[6]

#連線前準備，GW位置
# host = '10.10.1.223'
# user = 'octtel'
# Pass = '12841302'
#排除網站阻擋
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = { 'User-Agent' : user_agent}
#連線控制與URL
systeminformation_url = '/goform/StatusLoad'
systeminformation = 'FORM=SystemInformationForm'
data = '123'

#-----------------------------------------------------------------------------------------
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
	return data, http_data
	
	
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
	return data, http_data
#-----------------------------------------------------------------------------------------	

# 功能區

#-----------------------------------------------------------------------------------------	
# login
def login():
	login_url = '/goform/LoginForm'
	login_pass = 'username='+user+'&password='+Pass
	url = "/LoginForm.asp"
	useless1 = http_get(prot,url)
	url = login_url
	params = login_pass
	login_page = http_post(prot,url,params)
	print 'Login...'
	time.sleep(1)
	url = "/LoginFirstPageForm.asp"
	useless2 = http_get(prot,url)

# get status MAC, HW, Driver, Firmware
def status():
	url = '/goform/StatusLoad'
	params = 'FORM=SystemInformationForm'
	getinformation,x = http_post(prot,url,params)
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
	# firmware_long sample 1.2.38.99.440 2017/01/13 15:24:53) PId(901.CUBRelay.drtp) Drv(1.2.9.2921) Hw(IXP_PSTN808)
	# print firmware_long
	firmware_tail = firmware_long.find(' ')
	firmware_short = firmware_long[:firmware_tail]
	# firmware_short sample 1.2.38.99.440
	# print firmware_short
	build_head = firmware_short.rfind('.')
	build = firmware_short[build_head+1:]
	return mac, firmware_long, firmware_short, build


# UI command firmware upgrade with http server
def upgrade1():
	url = '/goform/UpgradeForm'
	params = 'K643_0=3&K122_0=192.168.1.123&K123_0=80&K645_0=&K646_0=&K124_0=&K638_0=0'
	upgrade_params = http_post(prot,url,params)
	url = '/goform/UpgradeLoadForm'
	# 一般GW使用url Form，跟CUB不同，最好增加upgrade_params的return判斷式共用function
	params = 'FORM=UpgradeurlForm&IS_UPGRADE=UPGRADE&UPGRADE_MODE='
	upgrade_page = http_post(prot,url,params)
	print upgrade_page
	
def upgrade():
	url = '/goform/UpgradeForm'
	# tftp K643_0=0
	# params = 'K643_0=0&K122_0=10.10.1.123&K123_0=69&K645_0=&K646_0=&K124_0=&K638_0=0'
	# http K643_0=3
	params = 'K643_0=3&K122_0=192.168.1.123&K123_0=80&K645_0=&K646_0=&K124_0=&K638_0=0'
	upgrade_params = http_post(prot,url,params)
	time.sleep(1)	
	url = '/goform/UpgradeLoadForm'
	# CUB 使用Sub Form，跟一般GW不同，最好增加判斷式共用function
	params = 'FORM=UpgradeSubForm&IS_UPGRADE=UPGRADE&UPGRADE_MODE='
	x,upgrade_page = http_post(prot,url,params)
	# print upgrade_page.status
	# correct return status is 200
	# 升級等待時間
	xx = 250
	print "Wait for "+str(xx)+" of sec."
	time.sleep(float(xx))

# save
def save():
	save_url = '/goform/RestartForm'
	save_params = 'FORM_INDEX=0&K48_0=1'
	url = save_url
	params = save_params
	save_page = http_post(prot,url,params)
	time.sleep(2)
	
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
	print "Restarting takes 70 sec."
	time.sleep(70)

# factory default
def factory():
	factory_url = '/goform/ConfigBackupLoadForm'
	factory_params = 'Config=ID_DefaultSetting'
	url = factory_url
	params = factory_params
	factory_page = http_post(prot,url,params)

# ping until reachable	
def ping(host):
	test = False
	# Ping parameters as function of OS
	ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
	# Ping    
	while test == False:
		test = os.system("ping " + ping_str + " " + host) == 0

# Get FXS line number
def SIP_page_FXS1():
	SIP_page_url = '/SipForm.asp'
	url = SIP_page_url
	SIP_page,x = http_get(prot,url)
	# str.find(str, beg=0, end=len(string))
	#"K10_0$分機$701|STRING","K10_1$分機$702|STRING"
	FXS_head = SIP_page.find('K10_0$分機$')
	FXS_tail = SIP_page.find('|',FXS_head+len('K10_0$分機$'))
	FXS1 = SIP_page[FXS_head+len('K10_0$分機$'):FXS_tail]
	return FXS1
#-----------------------------------------------------------------------------------------

# 主程式區

#-----------------------------------------------------------------------------------------

while True:
	login()
	# get status MAC, HW, Driver, Firmware
	mac, firmware_long, firmware_short, build = status()
	print host, mac, firmware_long, build
	if build == build_check:
		print "Firmware Complete!!!"
		factory()
		print "factory defaulted"
		save()
		print "Saved"
		FXS1 = SIP_page_FXS1()
		print "FXS number is "+FXS1
		break
	else:	
		print "Upgrading firmware"
		upgrade()
		# ping for restart
		ping(host)
		time.sleep(10)

print "Done ! Ring FXS"
FXS_ring = 'start sip_invite.exe '+FXS1+' '+host+' 5060'
p = subprocess.Popen(FXS_ring, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
time.sleep(10)

# except KeyboardInterrupt:
	# print '\n[*] User Request Shutdown'
	# print '[*] Quitting...'
	# sys.exit(1)