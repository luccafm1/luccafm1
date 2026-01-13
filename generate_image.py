import requests
from PIL import Image, ImageDraw, ImageFont
import os

USERNAME = "luccafm1"
SOURCE_IMAGE_PATH = "source_image.png"
OUTPUT_IMAGE_PATH = "follower_quote.png"
FONT_PATH = "font.ttf"
FONT_SIZE = 35
TEXT_COLOR = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 3

def get_follower_count(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("followers", 0)
    except requests.exceptions.RequestException:
        return None

def create_image(count):
    text = f"You don't get to {count} followers on Github\nwithout making some enemies"
    try:
        image = Image.open(SOURCE_IMAGE_PATH)
    except FileNotFoundError:
        return

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.multiline_textbbox((0, 0), text, font=font, stroke_width=STROKE_WIDTH)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    image_width, image_height = image.size
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center", stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)

    image.save(OUTPUT_IMAGE_PATH)

if __name__ == "__main__":
    followers = get_follower_count(USERNAME)
    if followers is not None:
        create_image(followers)
