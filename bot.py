import os
import time
import random
import traceback
from pathlib import Path
from PIL import Image, ImageDraw


import httpx
from pyrogram import Client, api


def remap(OldValue):
    OldMax = 255
    OldMin = 0
    NewMax = 9
    NewMin = 0
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    return round((((OldValue - OldMin) * NewRange) / OldRange) + NewMin)


def fetch_new_pic():
    API_URL = 'https://avatars1.githubusercontent.com/u/35767464?s=460&u=3af6a5623f45634808d990e195d71e58860a60dc&v=4'
    
    r = httpx.get(API_URL, stream=True)
    
    profile_photo = Path('profile_photo.jpg')
    
    with open(profile_photo, 'wb') as f:
        for chunk in r.stream():
            f.write(chunk)
    
    return profile_photo


def get_w_h_a(image):
    w, h = image.size
    a = float(h)/float(w)
    return w, h, a


def resize(image, new_width, new_height=None):
    old_width, old_height, aspect_ratio = get_w_h_a(image)
    if new_height is None:
        new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


def random_pixel():
    return random.randint(100, 720)


def modify(image):
    ASCII_CHARS = '@%#*+=-:. '
    new_pixels = [ASCII_CHARS[remap(pixel_value)] for pixel_value in image.getdata()]
    return ''.join(new_pixels)


def convert2text(image, new_width=720):
    image = resize(image, new_width)
    
    image = image.convert('L')
    
    pixels = modify(image)

    new_image = [pixels[index:index+new_width] for index in range(0, len(pixels), new_width)]
    
    return '\n'.join(new_image)


def ascii_pic(pic, pixel):
    image = Image.open(pic)
    target_file = Path('ascii_profile_photo.jpg')
    old_width, old_height, a = get_w_h_a(image)
    if old_width > 720:
        old_width = 720
        old_height = int(a * old_width)
    txt = convert2text(image, pixel)

    d = ImageDraw.Draw(image)

    dim = d.multiline_textsize(txt)
    img = Image.new('RGB', dim, 'white')
    d = ImageDraw.Draw(img)
    d.multiline_text((0,0), txt, fill=(0,0,0))
    img = resize(img, old_width, old_height)
    img.save(target_file, 'JPEG')
    pic.unlink()
    return target_file


def initiate_pic_updation(app):
    
    try:
        pic = fetch_new_pic()
    
        app.set_profile_photo(pic)
        pixel = random_pixel()
        
        pic = ascii_pic(pic, pixel) # https://github.com/RameshAditya/asciify || https://www.tutorialspoint.com/converting-an-image-to-ascii-image-in-python
        
        time.sleep(10)
        app.send_photo('me', pic)
        
        app.set_profile_photo(pic)
        
        pic.unlink()
    except:
        traceback.print_exc()



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
