import asyncio
import logging
import os
import threading
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'
string_session = "1BVtsOHYBuxXWOSoRUYuPL6Hr_MuCZjkm1eIXwNPCJwsHg3qRIg1aE55rn6BA83lNAuXRE00DGmjWesDzhqMarkD84ffWZlmHMwZPtmetKFv1G04bMcZ0DoVEi2RPwjNmRpIlotQrClfvd79e1SP53cJ6A_se8MMhAgblVtZFgZt7KpzkJzWrTwh-4b_9QVF5pVz0MUWgQ0AnwqxmD_Gzx_TPFl37S_fhBu0zR8BmNWgLVkv8_iij_FZ4HuEGw2_iHnYaQG8QyahSwMQ3jkWWwJI-T0ODGAkpMio3ko1ZDnwy1ZrqIF9fn7Y5f39Nx0O7ZkvwMMbTEECvtNeq3ODY2yXyZ8qNCSY="
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def main():
    await client.start()
    logger.info('''
 ___                   _______            _________________
|   |                /   ___   \         |______    _______|
|   |               /   /   \   \               |   |
|   |              /   /__ __\   \              |   |
|   |    ___      /   ________\   \             |   |
|   |___|   |    /   /         \   \      ______|   |______
\___________/   /___/           \___\    |_________________|
''')

async def send_riddle():
    while True:
        try:
            await client.send_message("@lustXcatcherrobot", "/riddle")
            response = await client.get_messages("@lustXcatcherrobot", limit=1)
            response_text = response[0].text
            logger.info(f"Received response: {response_text}")
            if "Please wait" in response_text:
                wait_time_match = re.search(r'Please wait (\d+) seconds', response_text)
                if wait_time_match:
                    wait_time = int(wait_time_match.group(1))
                    if wait_time == 0:
                        logger.info("Wait time is 0, sending immediately...")
                        continue  # Skip the sleep and send immediately
                    else:
                        logger.info(f"Waiting for {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
            else:
                logger.info("Waiting for 10 seconds (default)...")
                await asyncio.sleep(10)  # Default wait time if no specific wait time is found
        except Exception as e:
            logger.error(f"Error sending riddle: {e}")

@client.on(events.NewMessage(from_users="@lustXcatcherrobot"))
async def handle_new_message(event):
    if event.buttons:
        logger.info("Received buttons, clicking on them...")
        tasks = [button.click() for row in event.buttons for button in row]
        await asyncio.gather(*tasks)

def run_telegram_bot():
    client.loop.run_until_complete(main())
    client.loop.create_task(send_riddle())
    client.run_until_disconnected()

if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 10000)

    # Run the Telegram bot in a separate thread
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.daemon = True  # Set as daemon thread so it exits when main thread exits
    telegram_thread.start()

    # Run the Flask application
    app.run(host=HOST, port=PORT)
