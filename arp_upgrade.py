# coding=utf-8
from scapy.all import *
# windows compatibility issues for arp sniff
from scapy.arch.windows import compatibility
import sys

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
default_GW = '10.10.1.1'
MAC = '00:13:e8'
arp_result = ""
def arp_monitor_callback(pkt):
    # if ARP in pkt and pkt[ARP].op == 1 and pkt[ARP].pdst == '10.10.1.1' and pkt[ARP].hwsrc[0:8] == '00:13:e8':      
	# who-has(1), pdst = default_GW, hwsrc = MAC
	# if ARP in pkt and pkt[ARP].op == 1 and pkt[ARP].pdst == default_GW and pkt[ARP].hwsrc[0:8] == MAC: 
	if ARP in pkt and pkt[ARP].op in (1,2): 
		return pkt.sprintf("who has %pdst% ? Tell %ARP.psrc% %ARP.hwsrc%")
	

# sniff(prn=arp_monitor_callback, filter="arp")
while True:
	try:
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
		print "From sniff:"
		# Filter use Berkeley Packet Filter (BPF) syntax (the same one than tcpdump)
		# http://biot.com/capstats/bpf.html
# 檢查福億 mac address(00:0c:2a)
# match our IP address
		p=sniff(prn=arp_monitor_callback, filter="arp and dst host 10.10.1.1 and ether[6:4]&0xFFFFFF00==0x0013e800 or ether[0:4]&0xFFFFFF00==0x0013e800", store=1, count=1)

		# sniff(prn=arp_monitor_callback, filter="arp", count=1)

		# wrpcap('packetss.pcap', p)
		# for b in str(arp_result):
		# print "char: %s ord/value: %d hex: %x"%(b,ord(b),ord(b))


# print sniff
		print "From string:"
		#http://www.secdev.org/projects/scapy/doc/usage.html#hex-string
		print str(p[0].sprintf("%ARP.psrc% %ARP.hwsrc%"))		
		print '-------------------------------------------------------------------------'
# pass to 2ndary program

# KeyboardInterrupt
	except KeyboardInterrupt:
		print '\n[*] User Request Shutdown'
		print '[*] Quitting...'
		sys.exit(1)