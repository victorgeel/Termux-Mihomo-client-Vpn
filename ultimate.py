#!/usr/bin/env python3
import base64
import yaml
import os
import subprocess
import requests
import traceback
import shutil

RAW_URLS = [
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_BASE64.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/vmess",
    "https://raw.githubusercontent.com/Surfboardv2ray/v2ray-worker-sub/master/Eternity",
    "https://raw.githubusercontent.com/R-the-coder/V2ray-configs/main/config.txt"
]

CONFIG_DIR = os.path.expanduser("~/.config/mihomo")
OUTPUT_FILE = os.path.join(CONFIG_DIR, "config.yaml")
BACKUP_FILE = os.path.join(CONFIG_DIR, "config_backup.yaml")

USE_TELEGRAM = False
BOT_TOKEN = ""
CHAT_ID = ""

choice = input("Telegram notification သုံးမလား? (y/n): ").strip().lower()
if choice == "y":
    USE_TELEGRAM = True
    BOT_TOKEN = input("Bot Token ထည့်ပါ: ").strip()
    CHAT_ID = input("Chat ID ထည့်ပါ: ").strip()

os.makedirs(CONFIG_DIR, exist_ok=True)

def send_telegram_message(message):
    if not USE_TELEGRAM:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

def toast(message):
    subprocess.run(["termux-toast", message])

def download_raw_links():
    all_links = []
    for url in RAW_URLS:
        try:
            print(f"[INFO] Downloading from {url}")
            response = requests.get(url)
            if response.status_code == 200:
                lines = response.text.strip().splitlines()
                all_links.extend(lines)
            else:
                send_telegram_message(f"[အမှား] {url} မှ download မအောင်မြင်ပါ!")
        except:
            send_telegram_message(f"[အမှား] {url} မှ download error!")
    return all_links

def parse_vmess(link):
    try:
        data = base64.b64decode(link.replace("vmess://", "")).decode()
        config = yaml.safe_load(data)
        return {
            "name": config.get("ps", "vmess"),
            "type": "vmess",
            "server": config["add"],
            "port": int(config["port"]),
            "uuid": config["id"],
            "alterId": int(config.get("aid", 0)),
            "cipher": "auto",
            "tls": config.get("tls", "") == "tls"
        }
    except:
        return None

def parse_ss(link):
    try:
        link = link.replace("ss://", "")
        if "#" in link:
            link, name = link.split("#", 1)
        else:
            name = "shadowsocks"
        decoded = base64.b64decode(link.split("@")[0]).decode()
        method, password = decoded.split(":")
        server, port = link.split("@")[1].split(":")
        return {
            "name": name,
            "type": "ss",
            "server": server,
            "port": int(port),
            "cipher": method,
            "password": password
        }
    except:
        return None

def parse_trojan(link):
    try:
        link = link.replace("trojan://", "")
        parts = link.split("@")
        password = parts[0]
        server, port = parts[1].split(":")
        return {
            "name": "trojan",
            "type": "trojan",
            "server": server,
            "port": int(port),
            "password": password
        }
    except:
        return None

def health_check(proxy):
    try:
        url = "http://www.gstatic.com/generate_204"
        response = requests.get(url, timeout=3)
        return response.status_code == 204
    except:
        return False

def generate_config():
    proxies = []
    raw_links = download_raw_links()
    chunk_size = 1000
    for i in range(0, len(raw_links), chunk_size):
        chunk = raw_links[i:i+chunk_size]
        for line in chunk:
            line = line.strip()
            if line.startswith("vmess://"):
                p = parse_vmess(line)
            elif line.startswith("ss://"):
                p = parse_ss(line)
            elif line.startswith("trojan://"):
                p = parse_trojan(line)
            else:
                p = None
            if p and health_check(p):
                proxies.append(p)

    if not proxies:
        send_telegram_message("[အမှား] Proxy မတွေ့ပါ!")
        toast("Proxy မတွေ့ပါ!")
        return False

    if os.path.exists(OUTPUT_FILE):
        shutil.copy(OUTPUT_FILE, BACKUP_FILE)

    config = {
        "port": 7890,
        "socks-port": 8080,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "external-controller": "0.0.0.0:9090",
        "external-ui": "ui",
        "secret": "",
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "Auto-Select",
                "type": "url-test",
                "proxies": [p["name"] for p in proxies],
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300
            },
            {
                "name": "Manual-Select",
                "type": "select",
                "proxies": [p["name"] for p in proxies]
            }
        ],
        "rules": [
            "MATCH,Auto-Select"
        ]
    }

    with open(OUTPUT_FILE, "w") as out:
        yaml.dump(config, out)
    send_telegram_message(f"[အောင်မြင်] Config update! Proxy: {len(proxies)}")
    toast(f"Config update! Proxy: {len(proxies)}")
    return True

def restart_mihomo():
    subprocess.run(["pkill", "mihomo"])
    subprocess.Popen(["mihomo", "-d", CONFIG_DIR])
    send_telegram_message("[အောင်မြင်] Mihomo restart ပြီး!")
    toast("Mihomo restart ပြီး!")

def setup_cron():
    cron_line = f"0 * * * * {os.path.abspath(__file__)}"
    crontab_file = os.path.expanduser("~/.crontab")
    if os.path.exists(crontab_file):
        with open(crontab_file, "r") as f:
            if cron_line in f.read():
                return
    with open(crontab_file, "a") as f:
        f.write(cron_line + "\n")
    subprocess.run(["crontab", crontab_file])
    subprocess.run(["crond"])
    send_telegram_message("[အောင်မြင်] Cron job ထည့်ပြီး!")
    toast("Cron job ထည့်ပြီး!")

if __name__ == "__main__":
    try:
        if generate_config():
            restart_mihomo()
            setup_cron()
    except Exception as e:
        error_details = traceback.format_exc()
        send_telegram_message(f"[အလွန်အရေးကြီး အမှား]\n{error_details}")
        toast("အလွန်အရေးကြီး အမှား!")
