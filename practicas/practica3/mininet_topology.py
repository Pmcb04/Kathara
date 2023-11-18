#!/usr/bin/python
# -*- coding: utf-8 -*-

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


def myTopology():
    
    net = Mininet(topo=None, build=False, link=TCLink, controller=None)
    
    h1 = net.addHost('h1', ip='10.0.1.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.1.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.1.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.2.1/24', mac='00:00:00:00:00:04')
    h5 = net.addHost('h5', ip='10.0.2.2/24', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', ip='10.0.2.3/24', mac='00:00:00:00:00:06')
    h7 = net.addHost('h7', ip='151.100.37.12/24', mac='00:00:00:00:00:07')

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    net.addLink(s1, s2, cls=TCLink, bw=10)
    net.addLink(s2, s3, cls=TCLink, bw=10)
	
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h7, s2)
    net.addLink(h4, s3)
    net.addLink(h5, s3)
    net.addLink(h6, s3)
	
    net.start()

    h1.cmdPrint('route add default gw 10.0.1.254 h1-eth0')
    h2.cmdPrint('route add default gw 10.0.1.254 h2-eth0')
    h3.cmdPrint('route add default gw 10.0.1.254 h3-eth0')
    h4.cmdPrint('route add default gw 10.0.2.254 h4-eth0')
    h5.cmdPrint('route add default gw 10.0.2.254 h5-eth0')
    h6.cmdPrint('route add default gw 10.0.2.254 h6-eth0')
    h7.cmdPrint('route add default gw 151.100.37.254 h7-eth0')

    h1.cmdPrint('arp -s 10.0.1.254 00:00:00:00:11:11')
    h2.cmdPrint('arp -s 10.0.1.254 00:00:00:00:11:11')
    h3.cmdPrint('arp -s 10.0.1.254 00:00:00:00:11:11')
    h4.cmdPrint('arp -s 10.0.2.254 00:00:00:00:22:22')
    h5.cmdPrint('arp -s 10.0.2.254 00:00:00:00:22:22')
    h6.cmdPrint('arp -s 10.0.2.254 00:00:00:00:22:22')
    h7.cmdPrint('arp -s 151.100.37.254 00:00:00:00:33:33')

    h7.cmdPrint('sudo python3 -m http.server 80 &')
    
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myTopology()

