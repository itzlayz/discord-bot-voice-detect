import os
import disnake
import requests
import speech_recognition as sr
from pydub import AudioSegment
from disnake.ext import commands
from config import token, prefix

bot = commands.Bot(command_prefix=prefix, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot connected as {client.user}')

@bot.command()
async def detect(ctx):
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
