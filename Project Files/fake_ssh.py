#!/usr/bin/env python
"""Fake SSH Server Utilizing Paramiko"""
import threading
import socket
import sys
import traceback
import paramiko
from ip2geotools.databases.noncommercial import DbIpCity

PORT = 22
HOST = ''
LOG = open("logs/log.txt", "a")
HOST_KEY = paramiko.RSAKey(filename='keys/private.key')


LOGFILE = 'logins.txt' #File to log the user:password combinations to
IPLOGFILE = 'IP_logins.txt' #File to log the user:password combinations to
LOGFILE_LOCK = threading.Lock()



class FakeSshServer(paramiko.ServerInterface):
    """Settings for paramiko server interface"""
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            logfile_handle = open(LOGFILE,"a")
            print("New login: " + username + ":" + password)
            logfile_handle.write(username + ":" + password + "\n")
            logfile_handle.close()
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED
        # Declines all passwords as valid by default


    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def start_server():
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))

    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    while True:
        try:
            sock.listen(100)
            print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()

        logfile_handle = open(IPLOGFILE,"a+")
        print("New IP: " + addr[0])
        response = DbIpCity.get(addr[0].strip(), api_key='free')
        s=addr[0]+","+response.latitude+","+response.longitude+"\n"
        logfile_handle.write(s)
        logfile_handle.close()

        LOG.write("\n\nConnection from: " + addr[0] + "\n")
        print('Got a connection!')
        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(HOST_KEY)
            # Change banner to appear legit on nmap (or other network) scans
            transport.local_version = "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"
            server = FakeSshServer()
            try:
                transport.start_server(server=server)
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
                raise Exception("SSH negotiation failed")
            # wait for auth
            chan = transport.accept(20)
            if chan is None:
                print('*** No channel.')
                raise Exception("No channel")

            server.event.wait(10)
            if not server.event.is_set():
                print('*** Client never asked for a shell.')
                raise Exception("No shell request")

            chan.close()

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            traceback.print_exc()
            try:
                transport.close()
            except Exception:
                pass


if __name__ == "__main__":
    start_server()
