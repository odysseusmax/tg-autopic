import os
import time
from pathlib import Path


import httpx


def fetch_new_pic():
    API_URL = "https://source.unsplash.com/random"
    
    r = httpx.get(API_URL, stream=True)
    
    profile_photo = Path('profile_photo.jpg')
    
    with open(profile_photo, 'wb') as f:
        for chunk in r.stream():
            f.write(chunk)
    
    return profile_photo


def initiate_pic_updation(app):
    
    pic = fetch_new_pic()
    
    app.set_profile_photo(pic)
    
    pic.unlink()


def main():
    
    from pyrogram import Client
    
    from config import Config
    
    token = Config.USER_TOKEN
    
    app = Client(token,    api_id=Config.API_ID,    api_hash=Config.API_HASH)
    
    print('starting..')
    
    with app:
        while True:
            initiate_pic_updation(app)
            
            print('one more done..')
            
            time.sleep(70)
        
    print('stopped...')


if __name__ == "__main__":
    main()
