from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    COMMUNITY_NAME = "Дизайн Спільнота Одеси"

    INSTAGRAM = ""

    LUMA = ""

    GROUP_ID = 0