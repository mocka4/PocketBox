PocketBox 🧰
A tiny container runtime for learning container internals and security
PocketBox is a minimal, educational container runtime written in Python.

It is designed for learning, experimentation, and security research — not production use.
If Docker feels too big and opaque, PocketBox shows you what’s really going on.

⚠️ WARNING
PocketBox intentionally allows unsafe behaviors.
Do NOT expose containers to the internet.
Do NOT run on systems you care about.
This project is for:
Learning how containers work
Practicing container escape & command injection
Understanding /proc, process isolation, and runtime supervision
✨ Features
📦 Build images from a simple Pocketfile
▶ Run containers (foreground or supervised)
📊 Inspect container state
📜 View container logs
🧠 Execute commands inside running containers
🛑 Stop containers cleanly
🗑 Remove containers
🧪 Comes with intentionally vulnerable examples
📦 Installation
Requirements
Python 3.10+
Linux / Android (Termux works perfectly)
No root required
Download
Copy code
Bash
git clone https://github.com/mocka4/PocketBox.git
cd pocketbox
pip install -r requirements.txt
Or install locally:
Copy code
Bash
pip install -e .

🚀 Quick Start
1. Go to an example image
Copy code
Bash
cd images/cmdinj
2. Build the image
Copy code
Bash
python3 -m pocketbox.cli build
3. Run the container
Copy code
Bash
python3 -m pocketbox.cli run --supervised
4. See running containers
Copy code
Bash
python3 -m pocketbox.cli ps
5. Inspect it
Copy code
Bash
python3 -m pocketbox.cli inspect cmdinj-1
6. Trigger command injection
Copy code
Bash
curl --get --data-urlencode "c=id" http://127.0.0.1:<PORT>/cmd

📂 Pocketfile Format
Example:
Copy code
Text
FROM python
RUN pip install flask
COPY app.py /
CMD python3 app.py
Supported instructions:
FROM
RUN
COPY
CMD
🧪 Example Images
Located in images/
Image
Description
cmdinj
Deliberately vulnerable Flask app with command injection

🧠 How PocketBox Works (High Level)
Images are just folders
Containers are directories with:
PID file
Logs
Runtime metadata
Processes are launched directly via Python
Supervision restarts crashed containers
No namespaces, no cgroups — by design
Read more in docs/architecture.md.

❌ What PocketBox Is NOT
❌ Secure
❌ OCI compliant
❌ Docker-compatible
❌ Production-ready
🎯 Who This Is For
Security learners
CTF players
Reverse engineers
People curious about containers
Anyone who wants to see instead of abstract
📜 License
MIT — do whatever you want, just don’t blame me.