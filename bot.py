import requests
import time
import re
import json

BASE_URL = "https://www.ivasms.com"
EMAIL = "hiahemdhh@gmail.com"
PASSWORD = "Hh1234Hh"

BOT_TOKEN = "8754675585:AAHa-u4zg8JN318q2_CLzL0DHlZZKD2f7fA"
CHAT_ID = "-1003745034804"

CACHE_FILE = "cache.json"

session = requests.Session()


def load_cache():
    try:
        with open(CACHE_FILE,"r") as f:
            return set(json.load(f))
    except:
        return set()


def save_cache(cache):
    with open(CACHE_FILE,"w") as f:
        json.dump(list(cache),f)


def login():

    login_url = BASE_URL + "/login"

    r = session.get(login_url)

    token = ""

    if 'name="_token"' in r.text:
        token = r.text.split('name="_token" value="')[1].split('"')[0]

    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "_token": token
    }

    r = session.post(login_url,data=payload)

    if "/portal" in r.url:
        print("Login success")
        return True
    else:
        print("Login failed")
        return False


def get_sms():

    url = BASE_URL + "/portal/live/my_sms"

    r = session.get(url)

    return r.text


def extract_otp(text):

    codes = re.findall(r"\b\d{4,8}\b",text)

    return codes


def send_telegram(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id":CHAT_ID,
        "text":msg
    }

    requests.post(url,data=data)


cache = load_cache()

if not login():
    exit()

print("Bot started")

while True:

    try:

        html = get_sms()

        codes = extract_otp(html)

        for code in codes:

            if code not in cache:

                print("NEW OTP:",code)

                send_telegram(f"OTP Code: {code}")

                cache.add(code)

                save_cache(cache)

        time.sleep(5)

    except Exception as e:

        print("Error:",e)

        time.sleep(3)
