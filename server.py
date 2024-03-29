import socket
import sys
import json
from _thread import *
from gameobject import Terrain

from server_tcp import package
key = {
    'x': 323,
    'y': 677,
    'player': 0,
    'hp': 100,
    'missiles': [],
    'angle': 0,
    'speed': 3,
    'gold': 600
}

key_2 = {
    'x': 403,
    'y': 160,
    'player': 1,
    'hp': 100,
    'missiles': [],
    'angle': 0,
    'speed': 3,
    'gold': 600

}

keys_players = [key,key_2]


def threaded_client(conn, player):
    data_s = package.pack(keys_players[player])
    conn.send(data_s)
    reply = ""
    while 1:
        try:
            try:
                data_c = package.unpack(conn.recv(2048))
            except:
                break
            keys_players[player] = data_c
            if not data_c:
                print("Disconected")
                break
            else:
                if player == 1:
                    reply = keys_players[0]
                else:
                    reply = keys_players[1]
            data_s = package.pack(reply)
            conn.send(data_s)
        except socket.error as e:
            print(e)
            break
    print("Lost Connection ")
    conn.close()



def main(port,IP= '127.0.0.1'):
    HOST = IP
    PORT = int(port)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    try:
        s.bind((HOST,PORT))
    except socket.error as e:
        print(str(e))
    s.listen(2)
    print('Waiting for a connection, Server Started')
    currentPlayer = 0
    while 1:
        conn,addr = s.accept()
        print('Connectd to', addr)

        #th.Thread( target = threaded_client,args= (conn,)).start()
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


if __name__ == '__main__':
    main()
