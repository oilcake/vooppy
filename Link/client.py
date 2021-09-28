#!/usr/bin/env python3
import edn_format
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 17000        # The port used by the server


class Client():

    def __init__(self):
        self.ping()

    def ping(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'status')
            data = s.recv(1024)
            self.unpack(data)

    @staticmethod
    def decode_edn_msg(msg):
        """Decodes a TCP message from Carabiner to python dictionary"""
        msg = msg.decode()
        msg_type = msg[:msg.index(' {')]
        striped_msg = msg[msg.index('{'):]
        decoded_msg = edn_format.loads(striped_msg)

        # The edn_format package does not return normal dam dicts
        # (or string keywords). What dicts.
        if type(decoded_msg) is edn_format.immutable_dict.ImmutableDict:
            decoded_msg = {
                str(key).strip(':'): value for key,
                value in decoded_msg.dict.items()
            }
        return msg_type, decoded_msg

    def unpack(self, msg):
        msg_type, msg_data = self.decode_edn_msg(msg)

        if msg_type == 'status':
            self.bpm = msg_data['bpm']
            self.beat = msg_data['beat']
            self.start = msg_data['start']

        if msg_type == 'time_at_beat':
            self.next_beat = (msg_data['beat'], msg_data['when'])
