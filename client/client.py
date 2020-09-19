import telnetlib
import socket
import sys

delimiter = '@@@@@'.encode()

def send_bytes(data : bytes, sock : socket, print_progress=False):
    totalsent = 0
    while totalsent < len(data):
        sent = sock.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent += sent
        if print_progress:
            print('Sent {:.2%}'.format(totalsent / len(data)))    

def main():
    file_name = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    timeout = 100

    with telnetlib.Telnet(host, port, timeout) as session:
        sock = session.get_socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024) 
        with open(file_name, 'rb') as f:
            send_bytes(file_name.encode(), sock)
            send_bytes(delimiter, sock)

            msg = f.read()
            send_bytes(msg, sock, True)
        #with open(file_name, 'rb') as f:
            #session.write(file_name.encode())
            #session.write(delimiter)
            #session.write(f.read())


if __name__ == "__main__":
    main()