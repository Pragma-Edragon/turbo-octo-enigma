from os import path
from sys import argv
import aiohttp
import asyncio

import telethon
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import InputPhoto


'''
# HERE YOU CAN FIND YOUR OWN ID
# AND HASH FOR USING THIS APP
# https://my.telegram.org/

# FIRST ARGUMENT - API_ID,
# SECOND ARGUMENT- API_HASH
'''


def parse_args():
    if len(argv) != 3:
        print("No args specified")
        quit()
    else:
        api_id, api_hash = argv[1], argv[2]
        return api_id, api_hash


async def get_data(cli: telethon.TelegramClient, p, i=0):
    await get_cat()
    currentPhoto = ""
    if i > 0:
        currentPhoto = (await cli.get_profile_photos('me'))[0]
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
    await asyncio.sleep(10)
    i += 1
    await get_data(cli, p, i)


async def get_cat():
    with open("cat.png", 'wb') as file:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://thiscatdoesnotexist.com/') as resp:
                while True:
                    data = await resp.content.read(2048)
                    if not data:
                        break
                    file.write(data)


if __name__ == '__main__':
    pt = path.dirname(path.abspath(__name__))
    parse_args()
    client = telethon.TelegramClient("cat_session", *parse_args())
    with client:
        client.loop.run_until_complete(get_data(client, pt))
