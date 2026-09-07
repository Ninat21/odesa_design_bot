import os

from dotenv import load_dotenv

load_dotenv()


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} не знайдено в оточенні")
    return value


def required_int_list(name: str) -> tuple[int, ...]:
    value = required_env(name)

    try:
        values = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as error:
        raise RuntimeError(f"{name} має містити ID, розділені комами") from error

    if not values:
        raise RuntimeError(f"{name} не містить жодного ID")

    return values


class Config:
    BOT_TOKEN = required_env("BOT_TOKEN")

    API_ID = int(api_id) if (api_id := os.getenv("API_ID")) else None
    API_HASH = os.getenv("API_HASH")
    PHONE = os.getenv("PHONE")

    ADMIN_IDS = required_int_list("ADMIN_IDS")

    COMMUNITY_NAME = "Дизайн Спільнота Одеси"

    INSTAGRAM = ""

    LUMA = ""

    GROUP_ID = int(required_env("GROUP_ID"))


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
