import socket
from urllib.parse import parse_qs, urlparse


def parsereq(request_data):
    parts = request_data.split("\r\n\r\n", 1)
    header_part = parts[0]

    lines = header_part.split("\r\n")
    if not lines or lines[0] == "":
        return None

    first_line = lines[0].split(" ")
    if len(first_line) < 2:
        return None

    method = first_line[0]
    full_path = first_line[1]

    parsed_url = urlparse(full_path)
    path = parsed_url.path

    raw_query = parse_qs(parsed_url.query)
    querypar = {}
    for key, value in raw_query.items():
        if len(value) == 1:
            querypar[key] = value[0]
        else:
            querypar[key] = value

    return {
        "method": method,
        "path": path,
        "querypar": querypar,
    }




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