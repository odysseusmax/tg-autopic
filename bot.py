import os
import time
import datetime
from pathlib import Path


import httpx
from pyrogram import Client, api


def fetch_new_pic():
    API_URL = "https://picsum.photos/1280"
    
    r = httpx.get(API_URL, stream=True)
    
    profile_photo = Path('profile_photo.jpg')
    
    with open(profile_photo, 'wb') as f:
        for chunk in r.stream():
            f.write(chunk)
    
    return profile_photo


def fetch_fact():
    
    API_URL = "https://geek-jokes.sameerkumar.website/api"
    
    r = httpx.get(API_URL)
    
    data = r.text.replace('"', '')
        
    return data


def initiate_pic_updation(app):
    
    pic = fetch_new_pic()
    
    bio = fetch_fact()
    
    app.set_profile_photo(pic)
    
    tim = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(minutes=30, hours=5)))
    
    update_data = {}
                
    update_data.update({'first_name':f"{tim.hour}:{tim.minute} | {tim.day}-{tim.month}-{tim.year}"})
        
    update_data.update({'last_name': "odysseusmax"})
    
    if len(bio) <= 70:
        update_data.update({'about': bio})
        
    app.send(api.functions.account.UpdateProfile(**update_data))
    
    pic.unlink()



def main():
    
    from config import Config
    
    token = Config.USER_TOKEN
    
    app = Client(token,    api_id=Config.API_ID,    api_hash=Config.API_HASH)
    
    print('starting..')
    
    with app:
        while True:
            initiate_pic_updation(app)
            
            print('one more done..')
            
            time.sleep(75)
        
    print('stopped...')


if __name__ == "__main__":
    main()
