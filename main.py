import asyncio
import ast
from typing import List, Union

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.markdown import hlink

from config import TOKEN, ADDED_LINK, CHANNEL_ID, ALLOWED_USERS


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


class AlbumMiddleware(BaseMiddleware):

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


# start command handler
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        await message.reply(text='Hi, send me any messages, I will change them and post to the channel')
    else:
        await message.reply(text='You are not welcome here')


# text message handler
@dp.message_handler(is_forwarded=True, content_types=types.ContentType.TEXT)
async def text_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = message.text + ADDED_LINK
        await bot.send_message(chat_id=CHANNEL_ID, text=resend_message + source_link, disable_web_page_preview=True)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, content_types=types.ContentType.TEXT)
async def text_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = message.text + ADDED_LINK
        await bot.send_message(chat_id=CHANNEL_ID, text=resend_message + source_link, disable_web_page_preview=True)
    else:
        await message.reply(text='You are not welcome here')


# single photo handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.PHOTO)
async def photo_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_photo(chat_id=CHANNEL_ID, photo=message.photo[0]['file_id'], caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.PHOTO)
async def photo_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_photo(chat_id=CHANNEL_ID, photo=message.photo[0]['file_id'], caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# single video handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.VIDEO)
async def video_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
            if len(resend_message) > 1024:
                await bot.send_video(chat_id=CHANNEL_ID, video=message.video.file_id)
                await bot.send_message(chat_id=CHANNEL_ID, text=resend_message, disable_web_page_preview=True)
            else:
                await bot.send_video(chat_id=CHANNEL_ID, video=message.video.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.VIDEO)
async def video_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
            if len(resend_message) > 1024:
                await bot.send_video(chat_id=CHANNEL_ID, video=message.video.file_id)
                await bot.send_message(chat_id=CHANNEL_ID, text=resend_message, disable_web_page_preview=True)
            else:
                await bot.send_video(chat_id=CHANNEL_ID, video=message.video.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# video note handler
@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def video_note_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        await bot.send_video_note(chat_id=CHANNEL_ID, video_note=message.video_note.file_id)
    else:
        await message.reply(text='You are not welcome here')


# document handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.DOCUMENT)
async def document_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_document(chat_id=CHANNEL_ID, document=message.document.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.DOCUMENT)
async def document_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_document(chat_id=CHANNEL_ID, document=message.document.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# audio handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.AUDIO)
async def audio_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_audio(chat_id=CHANNEL_ID, audio=message.audio.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.AUDIO)
async def audio_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_audio(chat_id=CHANNEL_ID, audio=message.audio.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# animation handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.ANIMATION)
async def animation_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_animation(chat_id=CHANNEL_ID, animation=message.animation.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.ANIMATION)
async def animation_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_animation(chat_id=CHANNEL_ID, animation=message.animation.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# voice handler
@dp.message_handler(is_forwarded=True, is_media_group=False, content_types=types.ContentType.VOICE)
async def voice_forwarded(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_voice(chat_id=CHANNEL_ID, voice=message.voice.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=False, content_types=types.ContentType.VOICE)
async def voice_sent(message: types.Message):
    if message.chat.id in ALLOWED_USERS:
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        resend_message = ADDED_LINK
        if message.caption:
            resend_message = message.caption + ADDED_LINK
        await bot.send_voice(chat_id=CHANNEL_ID, voice=message.voice.file_id, caption=resend_message + source_link)
    else:
        await message.reply(text='You are not welcome here')


# media group handler
@dp.message_handler(is_forwarded=True, is_media_group=True, content_types=types.ContentType.ANY)
async def albums_forwarded(message: types.Message, album: List[types.Message]):
    if message.chat.id in ALLOWED_USERS:
        media_group = types.MediaGroup()
        if message.forward_from_chat and message.forward_from_chat.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from_chat.title, ('t.me/' + message.forward_from_chat.username))
        elif message.forward_from_chat and message.forward_from_chat.username is None:
            source_link = '\n\n🐘 Источник: ' + message.forward_from_chat.title
        elif message.forward_from and message.forward_from.username is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.forward_from.full_name, ('t.me/' + message.forward_from.username))
        else:
            source_link = '\n\n🐘 Источник: наш слон'
        for obj in album:
            if obj['caption'] is not None:
                resend_message = obj['caption'] + ADDED_LINK
                break
            else:
                resend_message = ADDED_LINK
        for obj in album:
            if obj.photo:
                file_id = obj.photo[-1].file_id
            else:
                file_id = obj[obj.content_type].file_id

            try:
                media_group.attach({"media": file_id, "type": obj.content_type})
            except ValueError:
                return await message.answer("This type of album is not supported by aiogram")
        if len(resend_message) < 1024:    
            string_media = str(media_group)  # превращаем в str наш экземпляр класса MediaGroup
            media_with_caption = ast.literal_eval(string_media)  # Превращаем str в list
            media_with_caption[0]['caption'] = resend_message + source_link
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_with_caption)
        else:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
            await bot.send_message(chat_id=CHANNEL_ID, text = resend_message + source_link, disable_web_page_preview=True)
    else:
        await message.reply(text='You are not welcome here')

@dp.message_handler(is_forwarded=False, is_media_group=True, content_types=types.ContentType.ANY)
async def albums_sent(message: types.Message, album: List[types.Message]):
    if message.chat.id in ALLOWED_USERS:
        media_group = types.MediaGroup()
        if message.from_user.full_name is not None:
            source_link = '\n\n🐘 Источник: ' + hlink(message.from_user.full_name, message.from_user.url)
        else:
            source_link = '\n\n🐘 Источник: ' + message.from_user.full_name
        for obj in album:
            if obj['caption'] is not None:
                resend_message = obj['caption'] + ADDED_LINK
                break
            else:
                resend_message = ADDED_LINK
        for obj in album:
            if obj.photo:
                file_id = obj.photo[-1].file_id
            else:
                file_id = obj[obj.content_type].file_id

            try:
                media_group.attach({"media": file_id, "type": obj.content_type})
            except ValueError:
                return await message.answer("This type of album is not supported by aiogram")
        if len(resend_message) < 1024:    
            string_media = str(media_group)  # превращаем в str наш экземпляр класса MediaGroup
            media_with_caption = ast.literal_eval(string_media)  # Превращаем str в list
            media_with_caption[0]['caption'] = resend_message + source_link
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_with_caption)
        else:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
            await bot.send_message(chat_id=CHANNEL_ID, text = resend_message + source_link, disable_web_page_preview=True)
    else:
        await message.reply(text='You are not welcome here')


if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)