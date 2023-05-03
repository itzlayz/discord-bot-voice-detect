import os
import disnake
import requests
import speech_recognition as sr
from time import time
from pydub import AudioSegment
from disnake.ext import commands
from config import token, prefix

bot = commands.Bot(command_prefix=prefix, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    
@bot.message_command()
async def detectVoiceText(inter: disnake.Interaction, msg: disnake.message.Message):
    if not msg.attachments:
        return await inter.response.send_message('There is no voice message', ephemeral=True)
    attachment = msg.attachments[0].url
    response = requests.get(attachment)
    tm = str(round(time()))

    print(type(inter), type(msg))
    
    with open(f'{tm}.ogg', 'wb') as f:
        f.write(response.content)

    audio = AudioSegment.from_file(f'{tm}.ogg', format='ogg')
    audio.export(f'{tm}.wav', format='wav')

    r = sr.Recognizer()
    with sr.AudioFile(f'{tm}.wav') as source:
        audio = r.record(source)
    
    #without it will be error (like timeout)
    await inter.response.send_message(f'Text from voice: Loading...')
    try:
        # you can change language, but it doesn't matter (maybe faster)
        text = r.recognize_google(audio, language='ru-RU')

        await inter.edit_original_response(f'Text from voice: {text}')
        os.remove(f'{tm}.ogg')
        os.remove(f'{tm}.wav')
    except sr.UnknownValueError:
        await inter.edit_original_response(f'Text not recognized')

@bot.command()
async def detect(ctx):
    if not ctx.message.reference:
        return await ctx.send('There is not a voice message')
    attachment = ctx.message.reference.resolved.attachments[0].url
    response = requests.get(attachment)
    name = ctx.author.name
    
    with open(f'{ctx.author.name}.ogg', 'wb') as f:
        f.write(response.content)

    audio = AudioSegment.from_file(f'{name}.ogg', format='ogg')
    audio.export(f'{name}.wav', format='wav')

    r = sr.Recognizer()
    with sr.AudioFile(f'{name}.wav') as source:
        audio = r.record(source)

    try:
        # you can change language, but it doesn't matter (maybe faster)
        text = r.recognize_google(audio, language='ru-RU')

        await ctx.reply(f'Text from voice: {text}')
        os.remove(f'{name}.ogg')
        os.remove(f'{name}.wav')
    except sr.UnknownValueError:
        await ctx.reply('Text not recognized')

bot.run(token)
