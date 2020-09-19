import socket
import random
import sys

delimiter = '@@@@@'.encode()

def send_bytes(data : bytes, sock : socket):
    totalsent = 0
    while totalsent < len(data):
        sent = sock.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent += sent

        print('Sent ', totalsent / len(data))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        file_name = sys.argv[1]
        dest_address = sys.argv[2]
        dest_port = int(sys.argv[3])
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192) 
        sock.bind(('localhost', 65432))
        sock.connect((dest_address, dest_port))
        with open(file_name, 'rb') as f:
            send_bytes(file_name.encode(), sock)
            send_bytes(delimiter, sock)

            msg = f.read()
            send_bytes(msg, sock)


if __name__ == "__main__":
    main()