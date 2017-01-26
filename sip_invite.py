# coding=utf-8
import socket, sys, random, time, os

def help():
	print 'sip_invite <Destination SIP> <Destination IP> <port> <Source SIP> <Source IP> <Source port>'
	print 'example:'
	# print 'sip_invite 701 10.10.1.162 5060 test 10.10.1.123 5060'
	print 'sip_invite 701 10.10.1.162 5060'
	os.system("pause")
	sys.exit()


if len(sys.argv) < 4:
	help()
target_SIP = sys.argv[1]
target_IP = sys.argv[2]
target_port = int(sys.argv[3])
# source_SIP = str(sys.argv[4])
# source_IP = str(sys.argv[5])
# source_port = sys.argv[6]


#test
# target_SIP = ''
# target_IP ='10.10.1.162'
# target_port = 5060
source_SIP = 'test'
#找到本機介面的IP位置
hostname = socket.gethostname()
source_IP = socket.gethostbyname(hostname)
source_port = '5060'
#raw_input
#搞一個亂數call-id，取隨機浮點數，刪除0.xxxxx，前2位數
Call_ID_ran = str(random.random())[2:]

sip_invite = ('INVITE sip:'+target_SIP+'@'+target_IP+';user=phone SIP/2.0\r\n'
# sip_invite = ('INVITE sip:'+target_IP+';user=phone SIP/2.0\r\n'
'Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,INFO,PRACK,REFER,SUBSCRIBE,NOTIFY,UPDATE,SERVICE\r\n'
'Via: SIP/2.0/UDP '+source_IP+':'+source_port+';branch=z9hG4bKd7436e21d8650617\r\n'
'From: ''"'+source_SIP+'"'' <sip:'+source_SIP+'@'+source_IP+'>;tag=e5c7825d-828\r\n'
'To: <sip:'+target_SIP+'@'+target_IP+';user=phone>\r\n'
# 'To: <sip:'+target_IP+';user=phone>\r\n'
'Call-ID: '+Call_ID_ran+'@SipHost\r\n'
'CSeq: 2 INVITE\r\n'
'Contact: <sip:'+source_SIP+'@'+source_IP+':'+source_port+'>\r\n'
'Expires:300\r\n'
'Max-Forwards:70\r\n'
'Remote-Party-ID: <sip:'+source_SIP+'@'+source_IP+'>;party=calling;privacy=off;screen=yes\r\n'
'Supported: replaces\r\n'
'User-Agent: 122 12-3898-13074-1.4.2.252-OGC200W\r\n'
'Content-Type: application/sdp\r\n'
'Content-Length: 0\r\n\r\n'
)
print sip_invite
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5.0)
client.bind (('0.0.0.0', 5060))
client.sendto(sip_invite,(target_IP,target_port))
data, addr = client.recvfrom(4096)
# print data
if data.find('180') > 0:
	print '1 Ringing'
	print data
	time.sleep(10)
else:
	client.sendto(sip_invite,(target_IP,target_port))
	data, addr = client.recvfrom(4096)
	if data.find('180') > 0:
		print '2 Ringing'
		print data
		time.sleep(10)
	else:
		print 'Invite fail'
		print data
		time.sleep(10)
# print 'END'
# print data