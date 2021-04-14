import asyncio
from os import path
from sys import argv

import telethon
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import InputPhoto

'''
# HERE YOU CAN FIND YOUR OWN ID
# AND HASH FOR USING THIS APP
# https://my.telegram.org/

# FIRST ARGUMENT - API_ID,
# SECOND ARGUMENT- API_HASH

# IF YOU USING VERSION WITH
# SELENIUM, PLEASE, USE DRIVER
# FROM HERE:
# https://chromedriver.chromium.org/downloads
'''


def parse_args():
    if len(argv) != 3:
        print("No args specified")
        quit()
    else:
        api_id, api_hash = argv[1], argv[2]
        return api_id, api_hash


async def get_data(cli: telethon.TelegramClient, p, i=0):
    await asyncio.get_event_loop().run_in_executor(None, get_cat)
    currentPhoto = ""
    if i > 0:
        currentPhoto = (await cli.get_profile_photos('me'))[0]
        print(currentPhoto)
    await cli(UploadProfilePhotoRequest(
        await cli.upload_file(p + "\cat.png")
    ))
    if len(str(currentPhoto)) != 0:
        await client(DeletePhotosRequest(
            id=[InputPhoto(
                id=currentPhoto.id,
                access_hash=currentPhoto.access_hash,
                file_reference=currentPhoto.file_reference
            )]
        ))
    await asyncio.sleep(5)
    i += 1
    await get_data(cli, p, i)


def get_cat():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://thiscatdoesnotexist.com/')
    driver.save_screenshot("cat.png")
    driver.close()

    img = Image.open("cat.png")
    newim = img.crop((150, 50, 650, 500))
    newim.save("cat.png")


if __name__ == '__main__':
    pt = path.dirname(path.abspath(__name__))
    parse_args()
    client = telethon.TelegramClient("cat_session", *parse_args())
    with client:
        client.loop.run_until_complete(get_data(client, pt))

