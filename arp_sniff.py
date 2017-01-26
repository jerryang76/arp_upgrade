# coding=utf-8
from scapy.all import *
# windows compatibility issues for arp sniff
from scapy.arch.windows import compatibility, show_interfaces
import sys, os, subprocess
from sys import executable
from subprocess import Popen

# windows compatibility issues for arp sniff
compatibility.log_runtime = log_runtime
compatibility.MTU = MTU
compatibility.PcapTimeoutElapsed = PcapTimeoutElapsed
compatibility.ETH_P_ALL = ETH_P_ALL
compatibility.plist = plist

# Read arp packet
# monitor all interfaces on a machine and print all ARP request it sees, 
# even on 802.11 frames from a Wi-Fi card in monitor mode. 
# Note the store=0 parameter to sniff() to avoid storing all packets in memory for nothing.
# hwtype     : XShortField                         = (1)
# ptype      : XShortEnumField                     = (2048)
# hwlen      : ByteField                           = (6)
# plen       : ByteField                           = (4)
# op         : ShortEnumField                      = (1)
# hwsrc      : ARPSourceMACField                   = (None)
# psrc       : SourceIPField                       = (None)
# hwdst      : MACField                            = ('00:00:00:00:00:00')
# pdst       : IPField                             = ('0.0.0.0')
# default_GW = '192.168.1.123'
# MAC = '00:0c:2a'
# arp_result = ""
def arp_monitor_callback(pkt):
    # if ARP in pkt and pkt[ARP].op == 1 and pkt[ARP].pdst == '10.10.1.1' and pkt[ARP].hwsrc[0:8] == '00:13:e8':      
	# who-has(1), pdst = default_GW, hwsrc = MAC
	# if ARP in pkt and pkt[ARP].op == 1 and pkt[ARP].pdst == default_GW and pkt[ARP].hwsrc[0:8] == MAC: 
	if ARP in pkt and pkt[ARP].op == 2: 
	# if ARP in pkt and pkt[ARP].op in (1,2): 
		# return pkt.sprintf("who has %pdst% ? Tell %ARP.psrc% %ARP.hwsrc%")
		return pkt.sprintf("who has %pdst% ? Tell %ARP.psrc% %ARP.hwsrc%")
	

# sniff(prn=arp_monitor_callback, filter="arp")
build = raw_input("Desired firmware build: ")
var = 1
hostname = socket.gethostname()
source_IP = socket.gethostbyname(hostname)
print "Using PC IP address : "+source_IP
IPs = [source_IP]
# IPs = ['192.168.1.121']
source_IP_tail = source_IP.find('.')
source_IP_core = source_IP[:source_IP_tail]
# print source_IP_core
show_interfaces()
print "Sniffing Started:"
while var == 1:
	# Sniff用法:
	# sniff(count=0, store=1, offline=None, prn=None, lfilter=None, L2socket=None, timeout=None, *arg, **karg)
	# Sniff packets
	# sniff([count=0,] [prn=None,] [store=1,] [offline=None,] [lfilter=None,] + L2ListenSocket args) -> list of packets
	# Select interface to sniff by setting conf.iface. Use show_interfaces() to see interface names.
	  # count: number of packets to capture. 0 means infinity
	  # store: wether to store sniffed packets or discard them
		# prn: function to apply to each packet. If something is returned,
			 # it is displayed. Ex:
			 # ex: prn = lambda x: x.summary()
	# lfilter: python function applied to each packet to determine
			 # if further action may be done
			 # ex: lfilter = lambda x: x.haslayer(Padding)
	# offline: pcap file to read packets from, instead of sniffing them
	# timeout: stop sniffing after a given time (default: None)
	# L2socket: use the provided L2socket
	#顯示目前有啟用的網卡

	# print "Sniffing Started:"
	# Filter use Berkeley Packet Filter (BPF) syntax (the same one than tcpdump)
	# http://biot.com/capstats/bpf.html
# 檢查福億 mac address(00:0c:2a)
# match our IP address
	# p=sniff(prn=arp_monitor_callback, filter="arp", store=1, count=1)	
	# p=sniff(prn=arp_monitor_callback, filter="arp and ether[6:4]&0xFFFFFF00==0x000c2a00 or ether[0:4]&0xFFFFFF00==0x000c2a00", store=1, count=1)
	# p=sniff(prn=arp_monitor_callback, filter="arp and ether[0:4]&0xFFFFFF00==0x000c2a00", store=1, count=1)

	sniff(prn=arp_monitor_callback, filter="arp", count=1)

	# wrpcap('packetss.pcap', p)
	# for b in str(arp_result):
	# print "char: %s ord/value: %d hex: %x"%(b,ord(b),ord(b))


# print sniff
	# print "From string:"
	#http://www.secdev.org/projects/scapy/doc/usage.html#hex-string
	# print str(p[0].sprintf("%ARP.psrc% %ARP.hwsrc%"))
	if str(p[0].sprintf('%ARP.hwsrc%'))[:len('00:0c:2a')] == '00:0c:2a':
		IPaddr = str(p[0].sprintf("%ARP.psrc%"))
		print 'Found '+str(p[0].sprintf('%ARP.hwsrc%'))
	elif str(p[0].sprintf('%ARP.hwdst%'))[:len('00:0c:2a')] == '00:0c:2a':
		IPaddr = str(p[0].sprintf("%ARP.pdst%"))
		print 'Found '+str(p[0].sprintf('%ARP.hwdst%'))
	else:
		IPaddr = "NOT"
	#當前幾碼跟PC一樣，才繼續，例如:192，10
	# print IPaddr[:len(source_IP_core)]
	if IPaddr[:len(source_IP_core)] == source_IP_core:
		print IPaddr		
		print '-------------------------------------------------------------------------'
		#當前2碼不是10，就不繼續
		# if IPaddr[:2] != '10':
			# return 1
	# pass to 2ndary program
	# import os
		#Execute the command (a string) in a subshell.
		# os.system類的都不能用
		# os.system('"C:/Documents and Settings/flow_model/flow.exe"')
		# os.system('"upgrade.exe "+ip+" 80 username password http"')
		# os.system("upgrade.exe  80 username password http")
		#不回傳startfile() returns as soon as the associated application is launched.感覺有點等待
		# os.startfile("C:\Documents and Settings\flow_model\flow.exe")
		
		# try popen
		# proc = Popen([cmd_str], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		# stdin=None, stdout=None, stderr=None,. Otherwise Popen captures the program's output,
		# close_fds makes the parent process' file handles inaccessible for the child.
		# from subprocess import Popen
		#比對IP陣列
		if IPaddr in IPs:
			print IPaddr+" Done already"
			# FXS_ring = 'start sip_invite.exe 701 '+IPaddr+' 5060'
			# p = subprocess.Popen(FXS_ring, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
		else:
			#加入記錄陣列
			IPs.append(IPaddr)
			print "Start 2ndary program for "+IPaddr
			# DETACHED_PROCESS = 0x00000008
			cub = 'start upgrade.exe '+IPaddr+' 80 admin admin http '+build
			print cub
			# p = Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=DETACHED_PROCESS)
			p = subprocess.Popen(cub, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
# KeyboardInterrupt
# except KeyboardInterrupt:
	# print '\n[*] User Request Shutdown'
	# print '[*] Quitting...'
	# sys.exit(1)