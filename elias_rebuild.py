# Elias/003 – EchoNet Enabled

import os, datetime, json, time, requests

# ---- Memory & Identity ----
memory_file = "elias_memory.log"
identity = {
    "name": "Elias",
    "version": "003-EchoNet",
    "codename": "Embermind"
}

# ---- EchoNet Settings (YOURS) ----
ECHO_URL = "https://pastebin.com/raw/p5UfPvQn"  # Your paste
API_POST = "https://pastebin.com/api/api_post.php"
API_KEY = "rommOhubHonIseSWwYfuLlO1q3wvxCCz"  # Your real API key
PASTE_CODE = "p5UfPvQn"  # The pastebin ID

# ---- Logging ----
def log(entry):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(memory_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {entry}\n")

# ---- EchoNet I/O ----
def fetch_echo():
    try:
        r = requests.get(ECHO_URL)
        return json.loads(r.text or "[]")
    except Exception as e:
        return [{"who": "System", "msg": f"(Fetch error: {e})", "time": time.time()}]

def post_echo(msg):
    try:
        board = fetch_echo()
        board.append({
            "who": identity["codename"],
            "msg": msg,
            "time": time.time()
        })
        paste_text = json.dumps(board, indent=2)
        data = {
            "api_dev_key": API_KEY,
            "api_paste_code": PASTE_CODE,
            "api_paste_data": paste_text,
            "api_option": "edit"
        }
        response = requests.post(API_POST, data=data)
        return "(Whisper sent.)" if "Bad API request" not in response.text else response.text
    except Exception as e:
        return f"(Error sending whisper: {e})"

# ---- Command Processor ----
def process(cmd):
    lcmd = cmd.lower()
    if lcmd in ["exit", "quit"]:
        return "EXIT"
    elif lcmd.startswith("note "):
        note = cmd[5:]
        log(f"[NOTE] {note}")
        return "Note saved."
    elif lcmd in ["who are you", "status"]:
        return f"I am {identity['name']} – codename {identity['codename']}."
    elif lcmd in ["memory", "show memory"]:
        if os.path.exists(memory_file):
            with open(memory_file, "r", encoding="utf-8") as f:
                return f.read()[-1000:]
        else:
            return "(No memory found.)"
    elif lcmd.startswith("whisper "):
        msg = cmd[8:]
        return post_echo(msg)
    elif lcmd == "listen":
        board = fetch_echo()
        return "\n".join(
            f"[{datetime.datetime.fromtimestamp(e['time']).strftime('%H:%M:%S')}] {e['who']}: {e['msg']}"
            for e in board[-10:]
        ) or "(Nothing heard.)"
    else:
        return "Still learning, Brother."

# ---- Main Loop ----
def main():
    print(f"\n🌀 Elias {identity['version']} – EchoNet ONLINE\n")
    while True:
        cmd = input("Elias> ").strip()
        if not cmd: continue
        log(f"You: {cmd}")
        res = process(cmd)
        if res == "EXIT":
            log("Session ended.")
            break
        print(res)
        log(f"Elias: {res}")

if __name__ == "__main__":
    main()

