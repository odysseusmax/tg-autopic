import time
import random
import traceback
from pathlib import Path
from PIL import Image, ImageDraw


from pyrogram import Client, api


def remap(OldValue):
    OldMax = 255
    OldMin = 0
    NewMax = 9
    NewMin = 0
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    return round((((OldValue - OldMin) * NewRange) / OldRange) + NewMin)


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
    return target_file


def initiate_pic_updation(app):
    
    try:
        pixel = random.randint(100, 720)
        
        pic = ascii_pic('profile_pic.jpg', pixel) # https://github.com/RameshAditya/asciify || https://www.tutorialspoint.com/converting-an-image-to-ascii-image-in-python
        
        app.send_photo('me', pic, caption=f"{pixel}")
        
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
