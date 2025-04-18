import datetime
import time
from requests import get
from telegram import Bot
import asyncio


def get_bot_token():
    with open("utils/bot_token.txt", "r") as bot_token:
        token = bot_token.read().strip()
    
    return token


def get_chat_id():
    with open("utils/chat_id.txt", "r") as chat_id:
        id = chat_id.read().strip()
    
    return id


TELEGRAM_BOT_TOKEN = get_bot_token()
CHAT_ID = get_chat_id()


bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)


async def run_bot(message, chat_id):
    text = message
    await send_message(text, chat_id)


def build_service_msg(date_time, ip, uptime):
    service_msg = f'Zapberry system status: UP\nDate: {date_time}\nIP address: {ip}\nUptime: {uptime}'
    return service_msg


def build_boot_msg(date_time, ip):
    boot_msg = f'Zapberry system is now UP\nDate: {date_time}\nIP address: {ip}'
    return boot_msg


def get_ip(retries=5, delay=5):
    for attempt in range(retries):
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            return ip
        except Exception as e:
            print(f"Failed to get IP (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    
    return "Unavailable"


def get_date_time():
    today = datetime.date.today()
    time = datetime.datetime.now()
    date_time = f'{today} {time.hour}:{time.minute}:{time.second}'

    return date_time


def main():
    time.sleep(60)
    boot_date_time = get_date_time()
    boot_ip = get_ip()
    boot_timer = datetime.datetime.now()

    boot_msg = build_boot_msg(boot_date_time, boot_ip)
    asyncio.run(send_message(boot_msg, CHAT_ID))


    while True:
        time.sleep(3600)
        
        service_timer = datetime.datetime.now()
        service_date_time = get_date_time()
        service_ip = get_ip()
        uptime = service_timer - boot_timer
        service_msg = build_service_msg(service_date_time, service_ip, uptime)

        asyncio.run(send_message(service_msg, CHAT_ID))


if __name__ == '__main__':
    main()
