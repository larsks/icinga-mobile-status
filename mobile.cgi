#!/usr/bin/python

import sys
import socket
import time

from Cheetah.Template import Template

SOCKET_PATH = '/var/icinga/rw/live'
BUFSIZE = 4096

def read_data(s):
    buffer = []
    while True:
        chunk = s.recv(BUFSIZE)
        if not chunk:
            break
        buffer.append(chunk)

    return ''.join(buffer)

def status (cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(SOCKET_PATH)
    s.send(cmd)
    s.shutdown(socket.SHUT_WR)
    response = read_data(s)
    s.close()

    return response

def get_host_status():
    hoststatus = status(
        'GET hosts\n'
        'Filter: notifications_enabled = 1\n'
        'Filter: acknowledged = 0\n'
        'Stats: state = 0\n'
        'Stats: state = 1\n'
        'Stats: state = 2\n'
        'Stats: state = 3\n'
    )
    hosts = dict(zip(
        ('up', 'down', 'unreachable', 'unknown'),
        [int(x) for x in hoststatus.split(';')]
        ))

    return hosts

def get_service_status():
    svcstatus = status(
        'GET services\n'
        'Filter: notifications_enabled = 1\n'
        'Filter: acknowledged = 0\n'
        'Stats: state = 0\n'
        'Stats: state = 1\n'
        'Stats: state = 2\n'
        'Stats: state = 3\n'
    )
    services = dict(zip(
        ('okay', 'warn', 'critical', 'unknown'),
        [int(x) for x in svcstatus.split(';')]
        ))

    return services

def results(hosts, services):
    t = Template.compile(open('/usr/share/icinga/templates/mobile.html').read())

    print 'Content-type: text/html'
    print
    print t(namespaces={
        'hosts': hosts,
        'services': services,
        'lastupdate': time.ctime()})

def main():
    hosts = get_host_status()
    services = get_service_status()
    results(hosts, services)

if __name__ == '__main__':
    main()

