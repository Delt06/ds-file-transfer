import telnetlib
import socket
import sys
import math

# delimiter to differentiate between data and file name
delimiter = '@@@@@'.encode()

# send a byte array via socket
def send_bytes(data : bytes, sock : socket):
    totalsent = 0
    while totalsent < len(data):
        sent = sock.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent += sent

def main():
    # read command line arguments
    file_name = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    timeout = 100

    # create a telnet session for convenice
    with telnetlib.Telnet(host, port, timeout) as session:
        # get telnet's underlying socket
        sock = session.get_socket()
        # open the file to send
        with open(file_name, 'rb') as f:
            # send file name
            send_bytes(file_name.encode(), sock)
            # send delimiter
            send_bytes(delimiter, sock)

            # read bytes from file
            msg = f.read()
            
            # divide the file into portions for better progress control
            portion_size = 2 << 15
            portions = math.ceil(len(msg) / portion_size)

            for i in range(portions):
                send_bytes(msg[i*portion_size:(i+1)*portion_size], sock)    
                # report current progress
                print('Sent {:.2%}'.format((i+1) / portions))


if __name__ == "__main__":
    main()