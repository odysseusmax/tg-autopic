import os
import json
import time
import random
from pathlib import Path


import httpx
from PIL import Image, ImageFont, ImageDraw


def fetch_qoute():
    api_url = "https://uselessfacts.jsph.pl/random.json"
    
    params = {'language': 'en'}
    
    r = httpx.get(api_url, params=params)
    
    responce_json = r.json()
        
    return responce_json.get('text')


def fetch_new_pic():
    RGB = [random.randint(1,255) for i in range (3)]
    
    size = 360, 360
    
    print(RGB)
    
    img = Image.new('RGB', size, RGB)
    
    image_path = Path('original_pic.jpg')
    
    img.save(image_path)
    
    return image_path, RGB
    


def combine(pic, qoute, fill):
    
    font = ImageFont.truetype("font.ttf", 30)
    
    out_file = Path("profile.jpg")

    img = Image.open(pic)
    
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    
    x, y = draw.textsize(text = qoute, font=font)
    
    cordinates = 0, 0
    
    draw.text(xy = cordinates, text = qoute,
                fill = fill, font=font,
                align="center"
        )        

    img.save(out_file)
    
    pic.unlink()
    
    return out_file


def initiate_pic_updation(app):
    
    pic, img_rbg = fetch_new_pic()
    
    qoute = fetch_qoute()
    
    fill = (255-i for i in img_rbg)
    
    processed_pic = combine(pic, qoute, fill)
    
    app.set_profile_photo(processed_pic)
    
    os.remove(processed_pic)


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
