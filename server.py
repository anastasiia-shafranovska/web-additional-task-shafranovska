import socket
from urllib.parse import parse_qs, urlparse
import json


def parsereq(requestdata):
    parts = requestdata.split("\r\n\r\n", 1)
    headerpart = parts[0]
    mainpart = parts[1] if len(parts) > 1 else ""

    lines = headerpart.split("\r\n")
    if not lines or lines[0] == "":
        return None

    first_line = lines[0].split(" ")
    if len(first_line) < 2:
        return None

    method = first_line[0]
    fullpath = first_line[1]

    parsedurl = urlparse(fullpath)
    path = parsedurl.path

    rawquery = parse_qs(parsedurl.query)
    querypar = {}
    for key, value in rawquery.items():
        if len(value) ==1:
            querypar[key]= value[0]
        else:
            querypar[key]=value
            

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, val = line.split(":", 1)
            headers[key.strip().lower()] = val.strip()
            

    jsonbody = None
    contenttype = headers.get("content-type", "")
    if mainpart and "application/json" in contenttype:
        try:
            jsonbody = json.loads(mainpart)
        except Exception:
            jsonbody = {"error": "Invalid JSON"}

    return {
        "method": method,
        "path": path,
        "querypar": querypar,
        "headers": headers,
        "body": jsonbody,
    }


def create_response(statcode, stattext, headers, mainbytes):
    resp = f"HTTP/1.1 {statcode} {stattext}\r\n"

    headers["Content-Length"] = str(len(mainbytes))
    headers["Connection"] = "close"

    for key, val in headers.items():
        resp += f"{key}: {val}\r\n"

    resp += "\r\n"

    return resp.encode("utf-8") + mainbytes




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
        data = clientsocket.recv(4096).decode("utf-8", errors="ignore")
        if data:
            req = parsereq(data)
            print("Parsed request:", req)

        response = create_response(
            200,
            "OK",
            {"Content-Type": "text/plain; charset=utf-8"},
            b"Response builder is working",
        )
        clientsocket.sendall(response)
        clientsocket.close()



if __name__ == "__main__":
    main()