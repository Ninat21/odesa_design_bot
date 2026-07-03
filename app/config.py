from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    ADMIN_IDS = [
        386918180, # Даша
        1411653442, # Саша
    ]

    COMMUNITY_NAME = "Дизайн Спільнота Одеси"

    INSTAGRAM = ""

    LUMA = ""

    GROUP_ID = 0

class Links:
    ABOUT = "https://t.me/c/2511970112/3732"
    INTRO = "https://t.me/c/2511970112/3667"

    CHAT = "https://t.me/c/2511970112/1"
    EVENTS = "https://t.me/c/2511970112/3634"
    COLLAB = "https://t.me/c/2511970112/3658"
    PROJECTS = "https://t.me/c/2511970112/3643"
    OFFTOP = "https://t.me/c/2511970112/3274"
    MEETUPS = "https://t.me/c/2511970112/2460"
    RESOURCES = "https://t.me/c/2511970112/1255"

    ADMIN_1 = "https://t.me/dashentsi_ya"
    ADMIN_2 = "https://t.me/art_by_mag"