#! /usr/bin/env python3.7

import ipaddress, sys

locale = False
ip = False
port = False

if len(sys.argv) > 1:
	try:
		ip = str(ipaddress.ip_address(sys.argv[1]))
	except ValueError:
		ip = False

if len(sys.argv) > 2:
	if int(sys.argv[2]) >=0 and int(sys.argv[2]) < 65536: port = sys.argv[2]

if len(sys.argv) > 3:
	if sys.argv[3] == "fr" or sys.argv[3] == "en": locale = sys.argv[3]

params = {
	"ip": ip,
	"port": port,
	"locale": locale
}

from game.main import main