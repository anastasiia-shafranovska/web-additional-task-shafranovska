import socket





def main():
    host = "127.0.0.1"
    port = 8080

    servsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servsocket.bind((host, port))
    servsocket.listen(5)

    print(f"Server started on http://{host}:{port}")

    while True:
        clientsocket, addr = servsocket.accept()
        print(f"Client connected from {addr}")

        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n Server is running!"
        clientsocket.sendall(response)
        clientsocket.close()


if __name__ == "__main__":
    main()