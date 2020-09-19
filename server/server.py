import socket
from threading import Thread
import os
import sys

# delimiter to differentiate between data and file name
delimiter = '@@@@@'.encode()

# a wrapper for client thread
class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
    
    def _close(self):
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        all_data = []
        while True:
            # receiving data in portions
            data = self.sock.recv(1024)

            if data: # received something
                all_data += list(data) # append it
            else: # finish receiving
                # using the delimiter, split data and file name
                (file_name, file_data) = ClientListener.split_by_delimiter(bytes(all_data))

                # if delimiter is present
                if file_name and file_data:
                    print(f'Received {file_name} ({len(file_data)}) bytes')
                    # get an unused file name
                    file_name = ClientListener.get_unused_file_name(file_name)
                    
                    # write file to disk
                    with open(file_name, 'wb') as f:
                        f.write(file_data)
 

                self._close()
                return

    @classmethod
    def split_by_delimiter(cls, data : bytes) -> (str, bytes):
        delimiter_len = len(delimiter)

        # searching fot the delimiter in data
        for i in range(len(data) - delimiter_len):
            part = data[i:i+delimiter_len]

            if bytearray(part) != bytearray(delimiter):
                continue

            # split by delimiter
            file_name = str(data[:i].decode())
            file_data = data[i+delimiter_len:]
            return (file_name, file_data)

        
        # report that the format is invalid
        print('Invalid format')
        return (None, None)

    # find a non-used file name
    @classmethod
    def get_unused_file_name(cls, file_name : str) -> str:
        # if not used at all, return the name itself
        if not os.path.exists('./' + file_name):
            return file_name

        # separate extension
        dot_index = file_name.rfind('.')
        extension = ''
        name = file_name

        if dot_index != -1:
            extension = file_name[dot_index + 1:] 
            name = file_name[:dot_index]
        
        num = 1
        file_path = ClientListener.get_full_file_name(name, num, extension)

        # trying to find an unused index
        while os.path.exists(file_path):
            num += 1
            file_path = ClientListener.get_full_file_name(name, num, extension)

        return file_path

    @classmethod
    def get_full_file_name(cls, name, num, extension):
        return './' + name + '_copy' + str(num) + '.' + extension


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', int(sys.argv[1])))
        sock.listen()
        while True:
            con, addr = sock.accept()
            print(str(addr) + ' connected')
            ClientListener(con).start()


if __name__ == "__main__":
    main()