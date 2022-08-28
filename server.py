import threading
import socket

from resource import Board

clients = []


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = Board()

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except socket.error:
        return print('\nIt was not possible to start server!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=messages_treatment, args=[client, r])
        thread.start()


def messages_treatment(client, r):
    while True:
        try:
            msg = client.recv(2048)
            print(f'message received: {str(msg)}')
            process_message(r, client, str(msg))
            # broadcast(msg, client)
        except socket.error:
            print(f'Something went wrong, error {e}')
            delete_client(client)
            break


def process_message(r, client, msg):
    if 'request' in msg:
        if r.request_resource(client):
            broadcast('accepted', client)
        else:
            broadcast('somebody are using the board, wait your turn', client)

    elif 'close' in msg:
        r.revoke_resource()
        broadcast('connection closed', client)
        if item := r.grant_resource():
            broadcast('accepted', item)


def broadcast(msg, client):
    print(f'message to broadcast: {msg}')
    for clientItem in clients:
        if clientItem == client:
            try:
                clientItem.send(msg.encode('utf-8'))
                break
            except Exception as e:
                print(e)
                delete_client(clientItem)


def delete_client(client):
    clients.remove(client)


main()
