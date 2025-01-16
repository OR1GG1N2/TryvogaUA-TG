from io import BytesIO

import requests
import structlog
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from PIL import Image
from fluent.runtime import FluentLocalization

# Declare router
router = Router()
router.message.filter(F.chat.type.in_(['group', 'supergroup'])) # process group events only

# Declare logger
logger = structlog.get_logger()

#
IMAGE_URL = "https://alert-node.vercel.app/api/map"

# Declare handlers
# @router.message(F.content_type.in_({'new_chat_members', 'left_chat_member'}))
# async def on_user_join_or_left(message: Message):
#     """
#     Removes "user joined" and "user left" messages.
#     By the way, bots do not receive left_chat_member updates when the group has more than 50 members (otherwise use https://core.telegram.org/bots/api#chatmemberupdated)
#     :param message: Service message "User joined group
#     """
#
#     await message.delete()

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



