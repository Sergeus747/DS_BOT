import discord
import asyncio
import os
import typing
import random                                               # радномайзер
import pafy
import json
from discord import *
from yandex_music import Client
from requests import get as r_get
from youtube_dl import YoutubeDL
from discord.ext import commands

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

with open("info.json", "r") as f:
    CONFIG = json.load(f)

TOKEN = CONFIG["TOKEN"]

bot = commands.Bot(command_prefix=('-'))
bot.remove_command( 'help' )
client = None
voice = None
Track_queue = []

Event = 0 # [1:Игра в кости; 2:]

class ROLL_GAME():               # Класс парной игры в кости
    Is_playing = False           # Идет ли игра
    players = ["",""]            # Имена игроков
    points = [0,0]               # Очки игроков
    Whose_throw = 0              # Кто бросает
    def reset(self):                 # Сброс игры в начальное состояние
        self.Is_playing = False
        self.points = [0,0]
        self.Whose_throw = 0
        return "Парные кости сброшены"

GAME_1 = ROLL_GAME()             # Создание объекта класса, отвечающего за парную игру в кости

rn = 0                           # рандомная переменная для выбора номера статьи


def search(URL):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: r_get(URL)
        except: info = ydl.extract_info(f"ytsearch:{URL}", download=False)['entries'][0]
        else: info = ydl.extract_info(URL, download=False)
    return (info, info['formats'][0]['url'])


@bot.event
async def on_ready():
    print("Я запущен!\n")


@bot.event
async def on_message(message): # Получение полного сообщения от бота
    print(f'Сообщение \n    Сервер: {message.guild.name}\n    Канал: {message.channel.name}\n    Имя автора: {message.author.name}\n    Содержание: {message.content}\n')
    await bot.process_commands(message)


@bot.command() # указываем боту на то, что это его команда
async def arg_test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

# A typing.Optional- это подсказка специального типа, которая допускает поведение «обратных ссылок». 
# Если конвертеру не удается выполнить синтаксический анализ в указанный тип, синтаксический анализатор пропустит параметр, 
# а затем Noneвместо этого в параметр будет передано указанное по умолчанию значение. Затем синтаксический анализатор перейдет 
# к следующим параметрам и конвертерам, если таковые имеются.

@bot.command() # указываем боту на то, что это его команда
async def bottles(ctx, amount: typing.Optional[int] = 99, *, liquid="beer"):
    await ctx.send('{} bottles of {} on the wall!'.format(amount, liquid))


@bot.command() # указываем боту на то, что это его команда
async def flip_coin(ctx):
    Coin = {                                            # Словарь
        0: "***Орел***",
        1: "***Решка***",
    }
    side_of_the_coin = random.randint(1, 1000)          # Радном от 1 до 1000, чтобы улучшить процентное соотношение выпадения разных вариантов
    # print(f'\n\nЧисло (1-1000): {side_of_the_coin}')
    await ctx.send(f'{Coin[side_of_the_coin%2]}')       # Вывод резуьтата броска(остаток от деления на 2)


@bot.command()                                          # указываем боту на то, что это его команда
async def condemn(ctx, *, condemned):                   # Осуждение: {author} осуждает {condemned}, по рандомной статье из словаря
    author = ctx.message.author.name                    # Получение имени автора запроса

    global previos, rn
    previos = rn
    rn = random.randint(1, 10)

    while previos == rn:
        rn = random.randint(1, 10)
    
    Article = {                                         # Словарь для статей
        1: "228 УК РФ: Незаконные приобретение, хранение, перевозка, изготовление переработка наркотических средств, психотропных веществ или их аналогов",
        2: "282 УК РФ: Возбуждение ненависти либо вражды, а равно унижение человеческого достоинства",
        3: "148 УК РФ: Нарушение права на свободу совести и вероисповеданий",
        4: "212.1 УК РФ: Неоднократное нарушение установленного порядка организации либо проведения собрания, митинга, демонстрации, шествия или пикетирования",
        5: "134 УК РФ: Половое сношение и иные действия сексуального характера с лицом, не достигшим шестнадцатилетнего возраста",
        6: "159.6 УК РФ: Мошенничество в сфере компьютерной информации",
        7: "119 УК РФ: Угроза убийством или причинением тяжкого вреда здоровью",
        8: "157 УК РФ: Неуплата средств на содержание детей",
        9: "201 УК РФ: Злоупотребление полномочиями",
        10: "666 УК РФ: Слишком жирная мамка"
    }
    Pictures = {                                        # Словарь для картинкок
        1: "https://media.discordapp.net/attachments/834330879828426762/834434025451683881/fb7d8dd74c882fc7.jpg",
        2: "https://lh6.googleusercontent.com/-dt9Sb1NJMkg/UfPBT6rMQUI/AAAAAAAABCw/6mSUNbvPGVw/w832-h553-no/DSC_1381.JPG",
        3: "https://i2.wp.com/pasmi.ru/wp-content/uploads/2018/07/631c75aed9594d9236de3cf6b6076641.jpg",
        4: "https://sun9-21.userapi.com/impf/c846121/v846121371/186ccc/NBz04AM-tTk.jpg?size=575x604&quality=96&sign=6d270eb395144c33a48eec64d4c4d37c&type=album",
        5: "https://i.ytimg.com/vi/9ylDGOlxLG4/maxresdefault.jpg",
        6: "https://sun9-74.userapi.com/impf/c855432/v855432298/426ab/PvvQMqR7GAQ.jpg?size=1280x856&quality=96&sign=79a8514df914fa8b7583516e31f85572&type=album",
        7: "https://avatars.mds.yandex.net/get-zen_doc/198334/pub_5b7f4d095b279900a96c2a40_5b7f6f4104a22900a90d7021/scale_2400",
        8: "https://www.prizyv.ru/wp-content/uploads/2019/12/alimenty.jpg",
        9: "https://i.pinimg.com/originals/cc/37/6d/cc376deb847316417dc0e28b956c50d3.jpg",
        10: "https://sun9-49.userapi.com/impf/c631631/v631631806/1ee6/xkDFNTarjSE.jpg?size=604x272&quality=96&proxy=1&sign=081ea4522fb0e450186eb23045007616&type=album"
    }
    Url_1 = discord.Embed()                             # Создание вложения
    Url_1.set_image(url=Pictures[rn]) 
    await ctx.message.delete()                          # Удаление запроса пользователя (чтобы не засорять канал)
    await ctx.send(f'{condemned} осужден по статье {Article[rn]}\n Брагодарю {author} за донесение!')   # Отправка сообщения
    await ctx.send(embed=Url_1)                         # Отправка вложения

@bot.command() # указываем боту на то, что это его команда
async def Roll_play(ctx, Enemy):
    global Event
    if Event == 0:
        GAME_1 .players[0] = ctx.message.author.mention
        GAME_1 .players[1] = Enemy
        Event = 1
        await ctx.send(f'{GAME_1.players[0]} вызывает {GAME_1.players[1]} на поединок!\nВсе решится тремя бросками кости, согласен ли {GAME_1.players[1]} принять вызов?\nДля ответ введите -Y или -N.')
        # my_file = open(имя_файла ,[ режим_доступа][, 0])
    else:
        await ctx.send(f'{ctx.message.author.mention} сейчас идет другая игра, дождитесь её окончания')

@bot.command() # указываем боту на то, что это его команда
async def Y(ctx):                                       # Принятие игры
    global Event
    # print(f'\n Номер ивента: {Event}   Состояние игры: {GAME_1.Is_playing}\n\n')
    if Event == 1 and GAME_1.Is_playing == False:
        if ctx.message.author.mention == GAME_1.players[1]:
            GAME_1.Is_playing = True                    # Начало игры           
            await ctx.send(f'{GAME_1.players[1]} принимает вызов! \nПервым бросок совершает {GAME_1.players[GAME_1.Whose_throw]}\nЧтобы совершить бросок напишите -Throw')
        else:
            await ctx.send(f'{ctx.message.author.mention} вас не вызывали на поединок, вы не можете согласиться')
    else:
        await ctx.send(f'{ctx.message.author.mention} сейчас идет другая игра, или игра вообще не запущена')


@bot.command() # указываем боту на то, что это его команда
async def N(ctx):                                       # Отказ от игры
    global Event
    # print(f'\n Номер ивента: {Event}   Состояние игры: {GAME_1.Is_playing}\n\n')
    if Event == 1 and GAME_1.Is_playing == False:
        if ctx.message.author.mention == GAME_1.players[1]:
            Event = 0                                   # Отмена ивента
            GAME_1.reset()                              # Сброс игры в начальное состояние            
            await ctx.send(f'{GAME_1 .players[1]} трусливо избегает поединка\nПобеда автоматически присуждается {GAME_1 .players[0]}')
        else:
            await ctx.send(f'{ctx.message.author.mention} вас не вызывали на поединок, вы не можете отказаться')
    else:
        await ctx.send(f'{ctx.message.author.mention} сейчас идет другая игра, или игра вообще не запущена')

@bot.command() # указываем боту на то, что это его команда
async def Throw(ctx):                                   # Бросок костей
    global Event
    Cube = {                                            # Словарь для картинкок
        1: '<:1_:834505302485237810>',
        2: '<:2_:834505302279192657>',
        3: '<:3_:834505302531113021>',
        4: '<:4_:834505302597828679>',
        5: '<:5_:834505302590095480>',
        6: '<:6_:834505302434119781>',
    }
    if Event == 1 and GAME_1.Is_playing == True:
        if  GAME_1.Whose_throw == 0 and ctx.message.author.mention == GAME_1.players[GAME_1.Whose_throw]:
            for number in [0, 1, 2]:
                Toss = random.randint(1, 6)
                GAME_1.points[GAME_1.Whose_throw] += Toss
                await ctx.send(f'{Cube[Toss]}')
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} твоё итоговое значение: {GAME_1.points[GAME_1.Whose_throw]}')
            GAME_1.Whose_throw += 1
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} твоя очедерь. Чтобы совершить бросок напиши -Throw')
        elif  GAME_1.Whose_throw == 1 and ctx.message.author.mention == GAME_1.players[GAME_1.Whose_throw]:
            for number in [0, 1, 2]:
                Toss = random.randint(1, 6)
                GAME_1.points[GAME_1.Whose_throw] += Toss
                await ctx.send(f'{Cube[Toss]}')
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} твоё итоговое значение: {GAME_1.points[GAME_1.Whose_throw]}')
            
            if GAME_1.points[0] > GAME_1.points[1]:
                await ctx.send(f'{GAME_1.players[0]} одержал победу! Несите Blackjack и зовите шлюх!')
                GAME_1.reset()                          # Сброс игры в начальное состояние
                Event = 0                               # Сброс номера ивента
            elif GAME_1.points[0] < GAME_1.points[1]:
                await ctx.send(f'{GAME_1.players[1]} одержал победу, Несите Blackjack и зовите шлюх!')
                GAME_1.reset()                          # Сброс игры в начальное состояние
                Event = 0                               # Сброс номера ивента
            else:
                GAME_1.points = [0,0]
                GAME_1.Whose_throw = 0
                await ctx.send(f'Получается ничья. Сыграем ещё?)\n{GAME_1.players[0]} бросай по новой!\nЧтобы совершить бросок напиши -Throw')
        else:
            await ctx.send(f'{ctx.message.author.mention} не твоя очередь.')
    else:
        await ctx.send(f'Нет активной игры')


@bot.command() # указываем боту на то, что это его команда
async def Stop_games(ctx):                              # Остановка всех игр (дополнять каждый раз, когда завозите новую игру!!!!!!!!!!!!!!!!!!!)
    global Event
    if Event == 0:
        await ctx.send(f'Нет запущенных игр.')
    else:
        GAME_1.reset()                                  # Сброс парных костей до базового состояния
        print(f'\n Номер ивента: {Event}   Состояние игры: {GAME_1.Is_playing}\n\n')
        # место дня новых ресеторв
        await ctx.send(f'{ctx.message.author.mention} сказал конец веселью, своравайте доски, прячьте кости.')
        Event = 0                                       # Сброс номера ивента
           

@bot.command() # указываем боту на то, что это его команда
async def naxuy(ctx):
    Url_1 = discord.Embed(
        title="Добро пожаловать!",
        description="Пройдите пожалйста нахуй",
        url='https://rt.pornhub.com',
    )
    await ctx.send(embed=Url_1)


@bot.command()
async def join(ctx):
    global voice
    try:
        if ctx.message.author.voice == None:
            await ctx.send(f'{ctx.message.author.mention}, может сначала ты на канал зайдешь?')
            return

        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except ClientException:
        await ctx.send(f'Ну не кричи ты так, тут я, тут...') 


@bot.command()                                          # указываем боту на то, что это его команда
async def Yanlog(ctx):                            # Логинимся в свой аккаунт Яндекса
    global client
    client = Client()
    # print(CONFIG["EMAIL"], CONFIG["PASSWORD"])
    client = Client.from_credentials(CONFIG["EMAIL"], CONFIG["PASSWORD"])
    # client.users_likes_tracks()[0].fetch_track().download('example.mp3')
    # await ctx.message.delete()                        # Удаление запроса пользователя (чтобы не палить личные данные данные)


@bot.command()                                          # указываем боту на то, что это его команда
async def Yandex_like_play(ctx, number, from_q = False):
    global client
    global voice
    global Track_queue

    if from_q:
        if Track_queue:
            number = Track_queue[0]
            Track_queue.remove(Track_queue[0])
        else:
            return
    try:
        os.system("rm example.mp3")
        client.users_likes_tracks()[int(number)].fetch_track().download('example.mp3')
    except:
        await ctx.send(f'{ctx.message.author.mention}, я такого трека не нашел, ты уверен что он есть?')
        return

    try:
        if ctx.message.author.voice == None:
            await ctx.send(f'{ctx.message.author.mention}, может сначала ты на канал зайдешь?')
            return

        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except ClientException:
        print(f'\nБот уже на канале, идем дальше\n')

    if voice.is_playing():
        Track_queue.append(number)
        await ctx.send(f'Там уже что-то бренькает, так и быть, добавлю в очередь')
    else:
        loop = asyncio.get_event_loop()
        await ctx.send(f'сейчас играет: {client.users_likes_tracks()[int(number)].fetch_track().artists_name()[0]}'\
        f': {client.users_likes_tracks()[int(number)].fetch_track().title}'\
        f' \nДлительность: {"{:.2f}". format(client.users_likes_tracks()[int(number)].fetch_track().duration_ms / 60000)} мин')    
        # print(f'\n\n{client.users_likes_tracks()[int(number)].fetch_track()}\n\n')
        voice.play(FFmpegPCMAudio('example.mp3'), after=lambda a: loop.create_task(Yandex_like_play(ctx, None, True))) # Запускаем трек, а по окончанию запускаем следующий из очереди
            


@bot.command()                                          # указываем боту на то, что это его команда
async def stop(ctx):
    global voice
    global Track_queue

    try:
        if voice.is_playing():
            Track_queue = []
            voice.stop()
            await ctx.send(f'Как скажешь {ctx.message.author.name}, выключаю')
    except:
        await ctx.send(f'Так там и не играет ничего, что пристал то?')

@bot.command()                                          # указываем боту на то, что это его команда
async def skip(ctx):
    global voice
    global Track_queue

    try:
        if voice.is_playing() and Track_queue:
            voice.stop()
            await ctx.send(f'{ctx.message.author.name} сказал следующий, как скажешь')
        elif voice.is_playing() and not Track_queue:
            voice.stop()
            await ctx.send(f'{ctx.message.author.name}, очередь пустая, так что я просто помолчу')
    except:
        await ctx.send(f'Так там и не играет ничего, что пристал то?')

@bot.command()                                          # указываем боту на то, что это его команда
async def pause(ctx):
    global voice

    try:
        if voice.is_playing() and not voice.is_paused():
            voice.pause()
            await ctx.send(f'Окей {ctx.message.author.name}, как скажешь, подожду пока\nКогда захочешь продолжить напиши -resume')
        elif voice.is_paused():
            await ctx.send(f'Так там и так на паузе, что пристал то?')
        else:
            await ctx.send(f'Так там и не играет ничего, что пристал то?')
    except AttributeError:
        await ctx.send(f'Так там и не играет ничего, что пристал то?')


@bot.command()                                          # указываем боту на то, что это его команда
async def resume(ctx):
    global voice

    try:
        if  voice.is_paused():
            voice.resume()
            await ctx.send(f'Продолжаем')
        elif voice.is_playing():
            await ctx.send(f'Так там и так играет, что пристал то?')
        else:
            await ctx.send(f'Нет треков на паузе, {ctx.message.author.name}, ты уверен что ставил что-то на паузу?')
    except AttributeError:
        await ctx.send(f'Нет треков на паузе, {ctx.message.author.name}, ты уверен что ставил что-то на паузу?')
    

@bot.command()
async def p(ctx, URL):
    global voice

    # Solves a problem I'll explain later
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(URL)
    # voice = utils.get(bot.voice_clients, guild=ctx.guild)

    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.mention}, может сначала ты на канал зайдешь?')
        return

    channel = ctx.author.voice.channel
    voice = await channel.connect()
    
    # await ctx.send(f"Now playing {info['title']}.")
    
    voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))


@bot.command()
async def leave(ctx):
    global voice
    global Track_queue
    try:
        Track_queue = []
        await ctx.voice_client.disconnect()
    except AttributeError:
        await ctx.send(f'Да ушел я уже, ушел, что ты такой злой?...')

bot.run(TOKEN)