#!/usr/bin/python

import sys
import socket
import time

from Cheetah.Template import Template

TITLE           = 'IRCS Monitoring'
SOCKET_PATH     = '/var/icinga/rw/live'
BUFSIZE         = 4096

def read_data(s):
    buffer = []
    while True:
        chunk = s.recv(BUFSIZE)
        if not chunk:
            break
        buffer.append(chunk)

    return ''.join(buffer)

def send_query (cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(SOCKET_PATH)
    s.send(cmd + '\n')
    s.shutdown(socket.SHUT_WR)
    response = read_data(s)
    s.close()

    return response

def livestatus (what, filters={}, stats=[]):
    cmdvec = [ 'GET %s' % what ]

    for k,v in filters.items():
        cmdvec.append('Filter: %s = %s' % (k,v))
        
    for k,v in stats:
        cmdvec.append('Stats: %s = %s' % (k,v))

    return send_query('\n'.join(cmdvec))

def get_host_status():
    hoststatus = livestatus('hosts',
        filters = dict(
            notifications_enabled=1,
            acknowledged=0,
            ),
        stats = (
            ( 'state', 0 ),
            ( 'state', 1 ),
            ( 'state', 2 ),
            ( 'state', 3 ),
            ))

    hosts = dict(zip(
        ('up', 'down', 'unreachable', 'unknown'),
        [int(x) for x in hoststatus.split(';')]
        ))

    return hosts

def get_service_status():
    svcstatus = livestatus('services',
        filters = dict(
            notifications_enabled=1,
            acknowledged=0,
            ),
        stats = (
            ( 'state', 0 ),
            ( 'state', 1 ),
            ( 'state', 2 ),
            ( 'state', 3 ),
            ))

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
        'lastupdate': time.ctime(),
        'title': TITLE})

def main():
    hosts = get_host_status()
    services = get_service_status()
    results(hosts, services)

if __name__ == '__main__':
    main()

