import socket
from urllib.parse import parse_qs, urlparse
import json
import os

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

    if not os.path.exists("public"):
        os.makedirs("public")

    if not os.path.exists("public/index.html"):
        with open("public/index.html", "w", encoding="utf-8") as f:
            f.write("<h1>Welcome to my Socket Server!</h1>\n<p>It works!</p>")

    while True:
        clientsocket, addr = servsocket.accept()

        try:
            data = clientsocket.recv(4096).decode("utf-8", errors="ignore")
            if not data:
                clientsocket.close()
                continue

            req = parsereq(data)
            if req is None:
                clientsocket.close()
                continue

            method = req["method"]
            path = req["path"]

            if method == "GET":
                if path == "/page":
                    page_id = req["querypar"].get("id", "Not specified")
                    html = f"<h2>Page Info</h2><p>ID: {page_id}</p>"
                    resp = create_response(
                        200,
                        "OK",
                        {"Content-Type": "text/html; charset=utf-8"},
                        html.encode("utf-8"),
                    )
                else:
                    filepath = (
                        "public/index.html" if path == "/" else f"public{path}"
                    )

                    if os.path.exists(filepath) and os.path.isfile(filepath):
                        with open(filepath, "rb") as f:
                            content = f.read()

                        contenttype = "text/html"
                        if filepath.endswith(".css"):
                            contenttype = "text/css"
                        elif filepath.endswith(".js"):
                            contenttype = "application/javascript"

                        resp = create_response(
                            200,
                            "OK",
                            {"Content-Type": f"{contenttype}; charset=utf-8"},
                            content,
                        )
                    else:
                        html_404 = "<h1>404 Not Found</h1>"
                        resp = create_response(
                            404,
                            "Not Found",
                            {"Content-Type": "text/html"},
                            html_404.encode("utf-8"),
                        )

            elif method == "POST":
                resdata = {
                    "message": "POST request received!",
                    "your_data": req["body"],
                    "your_headers": req["headers"],
                }
                jsonbytes = json.dumps(resdata, indent=2).encode("utf-8")
                resp = create_response(
                    200, "OK", {"Content-Type": "application/json"}, jsonbytes
                )

            else:
                resp = create_response(
                    405,
                    "Method Not Allowed",
                    {"Content-Type": "text/plain"},
                    b"Method Not Allowed",
                )

            clientsocket.sendall(resp)

        except Exception as e:
            print("Error handling request:", e)
        finally:
            clientsocket.close()



if __name__ == "__main__":
    main()