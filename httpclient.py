#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostname = url.split('://')[1]

	url2 = hostname.split('/')[0]
	host = socket.gethostbyname(url2)

	return (host,80)

    # creates a socket connected to host via port
    # REMEMBER TO CLOSE THE SOCKETS WHEN YOU USE THEM
    def connect(self, host, port):
        # use sockets!
	# sew the sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	# put on the sock
	sock.connect((host,port))
	print 'connected to ' + host, port
	return sock	

    def get_code(self, data):
        return data.split()[1]

    def get_headers(self,data):
	data = data.split('\r\n\r\n')
	data = data - data[-1]
        return data 

    def get_body(self, data):
        return data.split('\r\n\r\n')[-1]

    # read everything from the socket
    def recvall(self, sock):

        buffer = bytearray()
        done = False
        while not done:
	    try:
		part = sock.recv(1024)
		if (part):
		    buffer.extend(part)
		else:
		    done = not part
	    except:
		return str(buffer)
        return str(buffer)
    # Perform an HTTP GET request
    def GET(self, url, args=None):
        code = 200
	(http, uri) = re.split('://',url)
	target = ""	
	hostname = ""
	try:
	    hostname = uri.split('/')[0]
	    target = uri.split('/')[1]
	except:
	    hostname = uri
	    target = ""        
	
	body = "GET /"+target+"  HTTP/1.1 \r\nHost: "+hostname+" \r\n\r\n"
	host = ""
	port = 80
	try:
	    (host,port) = self.get_host_port(url)
	    sock = self.connect(host,port)
	    sock.sendall(body)
	    buff = self.recvall(sock)
	    code = self.get_code(buff)
	    body = self.get_body(buff)
	    if len(buff) == 0:
		code = 404
	    sock.close()
	except: 
	    code = 404
	
        return HTTPRequest(code, body)


    # Perform an HTTP POST request
    def POST(self, url, args=None): 
	code = 200
	(http, uri) = re.split('://',url)
	target = ""	
	hostname = ""
	try:
	    hostname = uri.split('/')[0]
	    target = uri.split('/')[1]
	except:
	    hostname = uri
	    target = ""        
	
	body = "POST "+ target +" / HTTP/1.1 \r\n content-type:application/x-www-form-urlencoded;charset=utf-8 \r\n Host: www."+hostname+" \r\n "
	try:	
	    query = re.split('\?', target)
	    query = query[1]
            body += len(query)+"\r\n" +query + '\r\n\r\n'
	except:
	    body += "\r\n"
	#sock_host = ""
	host = ""
	port = 80
	try:
	    (host,port) = self.get_host_port(url)
	    sock = self.connect(host,port)
	    sock.sendall(body)
	    buff = self.recvall(sock)
	    code = self.get_code(buff)
	    body = self.get_body(buff)
	    if len(buff) == 0:
		code = 404
	    sock.close()
	except: 
	    code = 404
	
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
