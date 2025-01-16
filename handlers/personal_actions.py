import structlog
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InputFile, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
from fluent.runtime import FluentLocalization

import io
from io import BytesIO
from PIL import Image

# Declare router
router = Router()
router.message.filter(F.chat.type == "private")

# Declare logger
logger = structlog.get_logger()
IMAGE_URL = "https://alert-node.vercel.app/api/map"


# Declare handlers
@router.message(Command("start"))
async def cmd_owner_hello(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("hello-msg"))


# Here is some example content types command ...
@router.message(F.content_type.in_({'photo', 'video'}))
async def cmd_media_react_bot(message: Message, l10n: FluentLocalization):
    await message.reply(l10n.format_value("media-msg"))



@router.message(F.text.lower().in_(['тривога', 'тревога']))
async def send_image_on_trigger(message: Message):
    response = requests.get(IMAGE_URL)
    response.raise_for_status()  # Проверяем, что запрос успешен

    with BytesIO(response.content) as image_stream:
        im = Image.open(image_stream).convert("RGBA")  # Оставляем прозрачность

        # Сохраняем в BytesIO
        output_stream = BytesIO()
        im.save(output_stream, format="webp", lossless=True)  # Поддержка прозрачности и без потерь
        output_stream.seek(0)  # Сброс указателя

        # Создаем BufferedInputFile
        sticker_file = BufferedInputFile(output_stream.getvalue(), filename="sticker.webp")

    # Отправляем как стикер
    await message.answer_sticker(sticker=sticker_file)