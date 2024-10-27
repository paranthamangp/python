'''
Instructions from : https://sujitpatel.in/article/how-to-send-telegram-message-with-python/

Step 1: Install python telegram bot using pip
pip install python-telegram-bot

Step 2: Create a Telegram bot
    (a) To use the Telegram API, you will need to create a Telegram bot and obtain its API key. You can do this by talking to the BotFather in Telegram. To do this:
    (b) Open the Telegram app on your smartphone or desktop.
    (c) Search for the “BotFather” username in the search bar.
    (d) Click on the “Start” button to start a conversation with the BotFather.
    (e) Type “/newbot” and follow the prompts to create a new bot. The BotFather will give you an API key that you will use in the next step.

'''

import asyncio
import telegram

#Token for 
TOKEN = 'TelegramToken'
chat_id = 'ChatId'


# Channel ID Sample: -1001829542722
bot = telegram.Bot(token=TOKEN)

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

'''
async def send_document(document, chat_id):
    async with bot:
        await bot.send_document(document=document, chat_id=chat_id)


async def send_photo(photo, chat_id):
    async with bot:
        await bot.send_photo(photo=photo, chat_id=chat_id)


async def send_video(video, chat_id):
    async with bot:
        await bot.send_video(video=video, chat_id=chat_id)
'''

async def main():
    # Sending a message
    await send_message(text='Test message from API', chat_id=chat_id)
    '''
    # Sending a document
    await send_document(document=open('/path/to/document.pdf', 'rb'), chat_id=chat_id)

    # Sending a photo
    await send_photo(photo=open('/path/to/photo.jpg', 'rb'), chat_id=chat_id)

    # Sending a video
    await send_video(video=open('path/to/video.mp4', 'rb'), chat_id=chat_id)
    
    '''

if __name__ == '__main__':
    asyncio.run(main())