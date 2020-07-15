import os
import time
from pathlib import Path
from PIL import Image, ImageDraw


import httpx
from pyrogram import Client, api


def fetch_new_pic():
    API_URL = "https://picsum.photos/720"
    
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


def grayscalify(image):
    return image.convert('L')


def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)


def do(image, new_width=1280):
    image = resize(image, new_width)
    
    image = grayscalify(image)
    
    width, _ = image.size

    pixels = modify(image)

    new_image = [pixels[index:index+width] for index in range(0, len(pixels), width)]
    
    return '\n'.join(new_image)


def ascii_pic(pic):
    ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
    image = Image.open(path)
    target_file = Path('ascii_profile_photo.jpg')
    old_width, old_height, a = get_w_h_a(image)
    if old_width > 720:
        old_width = 720
        old_height = int(a * old_width)
    txt = do(image)

    d = ImageDraw.Draw(image)

    dim = d.multiline_textsize(txt)
    img = Image.new('RGB', dim, 'white')
    d = ImageDraw.Draw(img)
    d.multiline_text((0,0), txt, fill='black')
    img = resize(img, old_width, old_height)
    img.save(target_file, 'JPEG')
    pic.unlink()
    return target_file


def initiate_pic_updation(app):
    
    pic = fetch_new_pic()
    
    app.set_profile_photo(pic)
    
    pic = ascii_pic(pic) # https://github.com/RameshAditya/asciify
    
    time.sleep(10)
    
    app.set_profile_photo(pic)
    
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
