#!/usr/bin/python

import sys
import socket
import time

from Cheetah.Template import Template

socket_path = "/var/icinga/rw/live"

def read_data(s):
    buffer = []
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        buffer.append(chunk)

    return ''.join(buffer)

def status (cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_path)
    s.send(cmd)
    s.shutdown(socket.SHUT_WR)
    response = read_data(s)
    s.close()

    return response

def main():
    hosts = { 'up': 0, 'down': 0, 'unreachable': 0, 'unknown': 0}
    services = { 'okay': 0, 'warn': 0, 'critical': 0, 'unknown': 0 }

    hoststatus = status("GET hosts\nColumns: state\nFilter: notifications_enabled=1")
    for st in hoststatus.split():
        if st == '0':
            hosts['up'] += 1
        elif st == '1':
            hosts['down'] += 1
        elif st == '2':
            hosts['unreachable'] += 1
        else:
            hosts['unknown'] += 1

    svcstatus = status("GET services\nColumns: state\nFilter: notifications_enabled=1")
    for st in svcstatus.split():
        if st == '0':
            services['okay'] += 1
        elif st == '1':
            services['warn'] += 1
        elif st == '2':
            services['critical'] += 1
        else:
            services['unknown'] += 1

    t = Template.compile(open('/usr/share/icinga/templates/mobile.html').read())
    print 'Content-type: text/html'
    print
    print t(namespaces={
        'hosts': hosts,
        'services': services,
        'lastupdate': time.ctime()})

if __name__ == '__main__':
    main()

