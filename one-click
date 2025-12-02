#!/usr/bin/env python3
import base64
import yaml
import os
import subprocess
import requests
import traceback
import shutil

# Multi-source raw URLs
RAW_URLS = [
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_BASE64.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/vmess",
    "https://raw.githubusercontent.com/Surfboardv2ray/v2ray-worker-sub/master/Eternity",
    "https://raw.githubusercontent.com/R-the-coder/V2ray-configs/main/config.txt"
]

CONFIG_DIR = os.path.expanduser("~/.config/mihomo")
OUTPUT_FILE = os.path.join(CONFIG_DIR, "config.yaml")
BACKUP_FILE = os.path.join(CONFIG_DIR, "config_backup.yaml")

# Telegram settings (dynamic)
USE_TELEGRAM = False
BOT_TOKEN = ""
CHAT_ID = ""

# Ask user for Telegram usage
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
    except Exception as e:
        print(f"[ERROR] Telegram မပို့နိုင်ပါ: {e}")

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
                send_telegram_message(f"[အမှား] {url} မှ download မအောင်မြင်ပါ! Status: {response.status_code}")
        except Exception as e:
            send_telegram_message(f"[အမှား] {url} မှ download error: {e}")
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
    except Exception:
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
    except Exception:
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
    except Exception:
        return None

def generate_config():
    proxies = []
    raw_links = download_raw_links()
    for line in raw_links:
        line = line.strip()
        if line.startswith("vmess://"):
            p = parse_vmess(line)
            if p: proxies.append(p)
        elif line.startswith("ss://"):
            p = parse_ss(line)
            if p: proxies.append(p)
        elif line.startswith("trojan://"):
            p = parse_trojan(line)
            if p: proxies.append(p)

    if not proxies:
        send_telegram_message("[အမှား] Proxy မတွေ့ပါ!")
        return False

    # Backup old config
    if os.path.exists(OUTPUT_FILE):
        shutil.copy(OUTPUT_FILE, BACKUP_FILE)
        print(f"[INFO] Backup saved to {BACKUP_FILE}")

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

    try:
        with open(OUTPUT_FILE, "w") as out:
            yaml.dump(config, out)
        send_telegram_message(f"[အောင်မြင်] Config update ပြီးပါပြီ! Proxy အရေအတွက်: {len(proxies)}")
        return True
    except Exception as e:
        send_telegram_message(f"[အမှား] Config သိမ်းမအောင်မြင်ပါ: {e}")
        return False

def restart_mihomo():
    try:
        subprocess.run(["pkill", "mihomo"])
        subprocess.Popen(["mihomo", "-d", CONFIG_DIR])
        send_telegram_message("[အောင်မြင်] Mihomo restart ပြီးပါပြီ")
    except Exception as e:
        send_telegram_message(f"[အမှား] Mihomo restart မအောင်မြင်ပါ: {e}")

if __name__ == "__main__":
    try:
        if generate_config():
            restart_mihomo()
    except Exception as e:
        error_details = traceback.format_exc()
        send_telegram_message(f"[အလွန်အရေးကြီး အမှား]\n{error_details}")
