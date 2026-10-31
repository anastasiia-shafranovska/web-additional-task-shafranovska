# Custom Python HTTP Server

A lightweight and custom HTTP server built from scratch in Python using the low-level `socket` library. The server parses raw incoming HTTP requests (extracting HTTP methods, paths, query parameters, headers, and JSON body) and constructs well-formatted HTTP responses.

## Features

* **Static File Serving:** Automatically creates a `public/` directory and serves `index.html` alongside CSS and JavaScript assets.
* **GET Routing:** Handles dynamic routes with query parameter parsing (e.g., `/page?id=...`).
* **POST Request Processing:** Receives JSON payloads and echoes data back in JSON format.
* **HTTP Status Codes:** Properly handles `200 OK`, `404 Not Found`, and `405 Method Not Allowed` responses.

## Getting Started

Run the server script using Python:

```bash
python server.py

Once running, navigate in your browser to: 
http://127.0.0.1:8080/

Example Routes
/ — Main page (serves public/index.html).

/page?id=123 — Dynamic page reading Query parameters.

/any-other-path — Triggers 404 Not Found.


## Testing POST Requests

### Windows PowerShell

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8080/" -Method POST -ContentType "application/json" -Body '{"user": "Anastasiia", "status": "testing"}'
cURL (Linux / macOS / Git Bash)
Bash
curl -X POST http://127.0.0.1:8080/ -H "Content-Type: application/json" -d '{"user":"Anastasiia"}'
