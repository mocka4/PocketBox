
from flask import Flask, request, render_template_string
import os, socket, sqlite3

app = Flask(__name__)

# -------------------------------
# Utility: random free port
# -------------------------------

from flask import Flask, request
import os, socket

app = Flask(__name__)

def find_free_port():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


# -------------------------------
# 1️⃣ COMMAND INJECTION (existing)
# Tool: Metasploit / Commix
# -------------------------------
@app.route("/cmd")
def cmd():
    return os.popen(request.args.get("c", "")).read()


# -------------------------------
# 2️⃣ SQL INJECTION
# Tool: sqlmap
# -------------------------------
@app.route("/login")
def login():
    user = request.args.get("user", "")
    pwd = request.args.get("pass", "")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # INTENTIONALLY VULNERABLE
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"
    result = cur.execute(query).fetchall()
    conn.close()

    if result:
        return "Login successful"
    return "Invalid credentials"

# -------------------------------
# 3️⃣ LOCAL FILE INCLUSION (LFI)
# Tool: Burp Suite / wfuzz
# -------------------------------
@app.route("/view")
def view():
    file = request.args.get("file", "")
    try:
        with open(file, "r") as f:
            return f.read()
    except:
        return "File not found"

# -------------------------------
# 4️⃣ SERVER-SIDE TEMPLATE INJECTION (SSTI)
# Tool: Burp Suite / manual browser testing
# -------------------------------
@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    template = f"Hello {name}"
    return render_template_string(template)

# -------------------------------
if __name__ == "__main__":
    port = find_free_port()
    print(f"[+] Vulnerable app listening on port {port}", flush=True)

if __name__ == "__main__":
    port = find_free_port()
    print(f"[+] Listening on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
