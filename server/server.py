import socket
from threading import Thread
import os

delimiter = '@@@@@'.encode()

clients = []

class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
    
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        all_data = []
        while True:
            data = self.sock.recv(1024)

            if data:
                all_data += list(data)
            else:
                (file_name, file_data) = ClientListener.split_by_delimiter(bytes(all_data))

                if file_name and file_data:
                    file_name = ClientListener.get_unused_file_name(file_name)
                    print(f'Received {file_name} ({len(file_data)}) bytes')
                    with open(file_name, 'wb') as f:
                        f.write(file_data)
 

                self._close()
                return

    @classmethod
    def split_by_delimiter(cls, data : bytes) -> (str, bytes):
        delimiter_len = len(delimiter)

        for i in range(len(data) - delimiter_len):
            part = data[i:i+delimiter_len]
            if bytearray(part) != bytearray(delimiter):
                continue

            file_name = str(data[:i].decode())
            file_data = data[i+delimiter_len:]
            return (file_name, file_data)

        
        print('Invalid format')
        return (None, None)

    @classmethod
    def get_unused_file_name(cls, file_name : str) -> str:
        if not os.path.exists('./' + file_name):
            return file_name

        dot_index = file_name.rfind('.')
        extension = ''
        name = file_name

        if dot_index != -1:
            extension = file_name[dot_index + 1:] 
            name = file_name[:dot_index]
        
        num = 1
        file_path = './' + name + '_copy' + str(num) + '.' + extension

        while os.path.exists(file_path):
            num += 1
            file_path = './' + name + '_copy' + str(num) + '.' + extension

        return file_path


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 8800))
        sock.listen()
        while True:
            con, addr = sock.accept()
            clients.append(con)
            print(str(addr) + ' connected')
            ClientListener(con).start()


if __name__ == "__main__":
    main()