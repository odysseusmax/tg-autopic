import json
import time
from pathlib import Path


import httpx


def fetch_qoute():
    api_url = "https://uselessfacts.jsph.pl/random.json"
    
    params = {'language': 'en'}
    
    r = httpx.get(api_url, params=params)
    
    responce_json = r.json()
        
    return responce_json.get('text')


def fetch_new_pic():
    api_url = "https://source.unsplash.com/random/300x300"
    
    r = httpx.get(api_url, stream=True)
    
    image_path = Path('original_pic.jpg')
    
    with open(image_path, 'wb') as f:
        for chunk in r.stream():
            f.write(chunk)
    
    return image_path


def combine(pic, qoute):
    
    font = ImageFont.truetype("font.ttf", 30)
    
    out_file = Path("profile.jpg")

    img = Image.open(pic)
    
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    
    x, y = draw.textsize(text = qoute, font=font)
    
    cordinates = width-(x+width/20), height-(y+height/20)
    
    draw.text(xy = cordinates, text = qoute,
                fill = (247,238,238), font=font,
                align="center"
        )        

    img.save(out_file)
    
    pic.unlink()
    
    return out_file


def initiate_pic_updation(app):
    
    pic = fetch_new_pic()
    
    qoute = fetch_qoute()
    
    processed_pic = combine(pic, qoute)
    
    app.set_profile_photo(processed_pic)
    
    processed_pic.unkink()


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
            
            time.sleep(65)
        
    print('stopped...')


if __name__ == "__main__":
    main()
