# Coded by Yashraj Singh Chouhan
import socket, threading  # Libraries import
from scraper import PyCrawler
import aes

#
#This is server of chat
#
#@author: Filip Werra s19375
#


host = '127.0.0.1'  # LocalHost
port = 7976  # Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
server.bind((host, port))  # binding host and port to socket
server.listen()

clients = []
nicknames = []
pwd = "pass"


def broadcast(message):  # broadcast function declaration
    for client in clients:
        #message = aes.AESCipher(pwd).encrypt(message)
        client.send(message)


def handle(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024)
            mess = client.recv(1024)
            #message = aes.AESCipher(pwd).decrypt(message)
            #if mess == "tajne":
            #    crawler = PyCrawler("https://www.marketviewliquor.com/blog/2018/08/how-to-choose-a-good-wine/")
            #    broadcast(crawler.start())
            #else:
            broadcast(message)
        except:  # removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():  # accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
