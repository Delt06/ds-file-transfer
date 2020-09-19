import telnetlib
import socket
import sys
import math

delimiter = '@@@@@'.encode()

def send_bytes(data : bytes, sock : socket):
    totalsent = 0
    while totalsent < len(data):
        sent = sock.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent += sent

def main():
    file_name = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    timeout = 100

    with telnetlib.Telnet(host, port, timeout) as session:
        sock = session.get_socket()
        with open(file_name, 'rb') as f:
            send_bytes(file_name.encode(), sock)
            send_bytes(delimiter, sock)

            msg = f.read()
            portion_size = 2 << 15
            portions = math.ceil(len(msg) / portion_size)

            for i in range(portions):
                send_bytes(msg[i*portion_size:(i+1)*portion_size], sock)    
                print('Sent {:.2%}'.format((i+1) / portions))


if __name__ == "__main__":
    main()