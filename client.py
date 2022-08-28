import threading
import socket
import time


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except socket.error:
        return print('\nIt was not possible connect with server!\n')

    username = input('User -> ')

    thread1 = threading.Thread(target=sendMessages, args=[client, username])
    thread2 = threading.Thread(target=receiveMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client, username):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(f'Server - {msg}\n')

            if 'accepted' in msg:
                print(f'YEAHH! I am using the board :D\n')
                time.sleep(15)
                sendMessages(client, username, 'close connection')

            elif 'closed' in msg:
                sendMessages(client, username)

        except socket.error:
            print('\nIt was not possible to keep connected with server!\n')
            print('Press <Enter> to continue...')
            client.close()
            break


def sendMessages(client, username, msg=None):
    if msg:
        client.send(msg.encode('utf-8'))
        return

    try:
        msg = input('Would you like to use the board? \n')
        if msg in ['sim', 'yes', 'si', 'ok', 'true', 'y']:
            client.send(f'request to user {username} on board'.encode('utf-8'))

    except:
        return


main()

# client sera avisado quando receber o recurso e contara um certo tempo
# quando este tempo encerrar client enviaria mensagem dizendo que finalizou