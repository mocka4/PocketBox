# 🧰 Pocketbox

**Pocketbox** is a lightweight, Docker‑like container runtime designed for **learning, security labs, CTFs, and environments where Docker is unavailable or overkill**.

It is especially useful on:
- 🐧 Linux
- 📱 Termux / Android
- 🧪 Pentesting & hacking labs
- 🎓 Learning environments

Pocketbox focuses on **simplicity, portability, and education**, not enterprise production workloads.

---

## 🚀 Why Pocketbox?

Docker is powerful — but it’s also:
- Heavy
- Complex
- Often unavailable on mobile or restricted systems

Pocketbox exists to solve a different problem.

### Pocketbox is:
✅ Simple  
✅ Lightweight  
✅ Easy to understand  
✅ Perfect for labs and experiments  

### Pocketbox is NOT:
❌ A Docker replacement  
❌ A production container runtime  
❌ Kubernetes‑compatible  

---

## 🧠 Mental Model

If you understand Docker, Pocketbox will feel familiar:

| Docker | Pocketbox |
|------|----------|
| Dockerfile | Pocketfile |
| docker build | pocketbox build |
| docker run | pocketbox run |
| docker ps | pocketbox ps |

But internally, Pocketbox is **simpler and more transparent**, making it ideal for learning.

---

## 📦 Installation

git clone https://github.com/mocka4/PocketBox.git
cd pocketbox
pip install -e .
