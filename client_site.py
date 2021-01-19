# Coded by Yashraj Singh Chouhan
import socket, threading
from scraper import PyCrawler
import aes

#
#This is client to test nulti client chat
#
#@author: Filip Werra s19375
#

nickname = input("Choose your nickname: ")
pwd = "pass"
#if nickname == "tajne":
#    crawler = PyCrawler("https://www.marketviewliquor.com/blog/2018/08/how-to-choose-a-good-wine/")
#    crawler.start()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server


def receive():
    while True:  # making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                #message = aes.AESCipher(pwd).decrypt(message).decode('utf-8')
                print(message)
        except:  # case on wrong ip/port details
            print("An error occured!")
            client.close()
            break


def write():
    while True:  # message layout
        mess = input('')
        message = '{}: {}'.format(nickname, mess)
        #message = aes.AESCipher(pwd).encrypt(message).decode('utf-8')
        client.send(message.encode('ascii'))
        client.send(mess.encode('ascii'))


receive_thread = threading.Thread(target=receive)  # receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)  # sending messages
write_thread.start()
