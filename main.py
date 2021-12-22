#!/usr/bin/env python3

import socket
import keyboard
from time import sleep
import argparse

HOST = 'localhost'
PORT = 29999

instructions="""
UR Dashboard Client
Shortcut keys:

a play
s pause
d stop
f programstate
v polyscopeversion

h display this help
q quit.
"""
commands={'a': 'play',
          's': 'pause',
          'd': 'stop',
          'f': 'programstate',
          'v': 'polyscopeversion'
          }

def show_instructions():
  print(instructions)

def send_command(command):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    status = s.recv(1024)
    s.sendall(command.encode() + b'\n')
    data = s.recv(1024)
  return data.decode()

  
def main():
  global HOST
  global PORT

  parser = argparse.ArgumentParser(description="Connect to an UR dashboard server. Specify settings.")
  parser.add_argument("host", help="the host ip")
  parser.add_argument("-p", "--port", type=int, help="the port number default 29999", default=29999)
  args = parser.parse_args()
  HOST = args.host
  PORT = args.port
  show_instructions()
  
  while True:
    in_command = keyboard.read_key(suppress=True)
    if in_command in commands.keys():
      command = commands.get(in_command)
      print(send_command(command))
    elif in_command == 'q':
      break
    else:
      show_instructions()
      print("Please enter valid key")
    sleep(0.1) 

if __name__ == '__main__':
  main()
