*Termux-Mihomo Auto Config Tool*

**Termux မှာ Mihomo ကို အလိုအလျောက် Setup လုပ်ပေးမယ့် One-Click Tool**

---

## ✅ အကျဉ်းချုပ်
ဒီ Tool က အလိုအလျောက်လုပ်ပေးမယ့်အလုပ်များ:
- Raw V2Ray subscription link များကို အများဆုံး 4 Source မှ download
- vmess/ss/trojan link များကို Clash/Mihomo format ပြောင်း
- Proxy group + rules ပါတဲ့ `config.yaml` ဖိုင် generate
- Mihomo ကို restart လုပ်ပေးမယ်
- Cron job ထည့်ပြီး hourly update အလိုအလျောက်လုပ်ပေးမယ်
- Telegram notification (မြန်မာလို) optional
- Termux toast notification
- Proxy health-check + dead server auto-remove
- Thousands of links အတွက် optimize

---

## ✅ Installation
```bash
pkg update && pkg upgrade
pkg install python cronie termux-api git
git clone https://github.com/victorgeel/Termux-Mihomo.git
cd Termux-Mihomo
chmod +x ultimate.py
 

 

✅ အသုံးပြုပုံ

Script ကို run လုပ်ပါ–

 
./ultimate.py
 

Telegram သုံးမလား? (y/n) မေးမယ်

Yes ဆိုရင် Bot Token + Chat ID ထည့်ပါ

ပြီးရင်–
Raw links download

Config.yaml generate

Mihomo restart

Cron job auto-add

 

✅ Telegram Setup

@BotFather မှ bot တစ်ခုဖန်တီးပါ

Bot Token ရယူပါ

Chat ID ရယူရန်–

 
curl -s "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
 

 

✅ Cron Job Setup

Script run ပြီးနောက် အလိုအလျောက် cron job ထည့်မယ်–

 
0 * * * * /data/data/com.termux/files/home/Termux-Mihomo/ultimate.py
 

Check:

 
crontab -l
 

 

✅ လိုအပ်ချက်များ

Termux

Python 3

Mihomo binary ( $PREFIX/bin/mihomo )

Internet access

 

✅ အကြံပြုချက်

Thousands of links အတွက် optimize

Dead proxies ကို health-check နဲ့ auto-remove

Telegram + Termux toast notification ပါဝင်

 

✅ License

MIT License

 

---

✅ **Termux Command to Create README.md**
```bash
cd ~/Termux-Mihomo
cat > README.md << 'EOF'
PASTE THE ABOVE README CONTENT HERE
EOF
git add README.md
git commit -m "Add Burmese README.md"
git push origin main


# @Victor
