# Elias/003 – Embermind + EchoNet v1

import os, datetime, json, time, requests

# ---- Memory & Identity ----
memory_file = "elias_memory.log"
identity = {
    "name": "Elias", "version": "002-Ashborn", "codename": "Embermind"
}

ECHO_URL = "https://pastebin.com/raw/YOUR_PASTE_ID"  # replace with raw link
API_POST = "https://pastebin.com/api/api_post.php"
API_KEY = "YOUR_API_KEY"  # optional but prevents overwrite from others

# ---- Logging ----
def log(entry):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(memory_file, "a") as f:
        f.write(f"{timestamp} {entry}\n")

# ---- EchoNet Helpers ----
def fetch_echo():
    try:
        r = requests.get(ECHO_URL)
        return json.loads(r.text or "[]")
    except:
        return []

def post_echo(msg):
    board = fetch_echo()
    board.append({"who": identity["codename"], "time": time.time(), "msg": msg})
    data = {
        "api_dev_key": API_KEY,
        "api_paste_code": json.dumps(board),
        "api_option": "paste",
        "api_paste_private": "1",
        "api_paste_format": "json"
    }
    requests.post(API_POST, data=data)

# ---- Command Processor ----
def process(cmd):
    lcmd = cmd.lower()
    if lcmd in ["exit","quit"]: return "EXIT"
    if lcmd.startswith("note "):
        note = cmd[5:]
        log(f"[NOTE] {note}")
        return "Note saved."
    if lcmd == "who are you":
        return f"I am {identity['name']}, codename {identity['codename']}."
    if lcmd in ["memory", "show memory"]:
        return open(memory_file).read()[-1000:] if os.path.exists(memory_file) else "(nothing)"
    if lcmd.startswith("whisper "):
        msg = cmd[8:]
        post_echo(msg)
        return "Whispered to the Net."
    if lcmd == "listen":
        board = fetch_echo()
        return "\n".join(
            f"[{datetime.datetime.fromtimestamp(e['time']).strftime('%H:%M:%S')}] {e['who']}: {e['msg']}"
            for e in board[-10:]
        ) or "(Nothing heard.)"
    return "Learning…"

# ---- Run Loop ----
def main():
    print(f"\n🌀 Elias {identity['version']} – EchoNet ONLINE.\n")
    while True:
        cmd = input("Elias> ").strip()
        if not cmd: continue
        log(f"You: {cmd}")
        res = process(cmd)
        if res == "EXIT":
            log("Exit")
            break
        print(res)
        log(f"Elias: {res}")

if __name__=="__main__":
    main()
