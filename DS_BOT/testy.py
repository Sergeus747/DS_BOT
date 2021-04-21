import discord
import typing
import random                                               # радномайзер
import pafy
import json
from discord import *
from requests import get as r_get
from youtube_dl import YoutubeDL
from discord.ext import commands

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

with open("DS_BOT/info.json", "r") as f:
    CONFIG = json.load(f)

TOKEN = CONFIG["TOKEN"]

bot = commands.Bot(command_prefix=('-'))
bot.remove_command( 'help' )

global vc
Event = 0 # [1:Игра в кости; 2:]

class ROLL_GAME():
    Is_playing = False           # Идет ли игра
    players = ["",""]            # Имена игроков
    points = [0,0]               # Очки игроков
    Whose_throw = 0              # Кто бросает

GAME_1 = ROLL_GAME()

rn = 0


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


@bot.command()                                          # указываем боту на то, что это его команда
async def condemn(ctx, *, condemned):                   # Осуждение: {author} осуждает {condemned}, по рандомной статье из словаря
    author = ctx.message.author.name                    # Получение имени автора запроса

    global previos, rn
    previos = rn
    rn = random.randint(1, 10)

    while previos == rn:
        rn = random.randint(1, 10)
    
    Article = {                                         # Словарь для статей
        1: "228 УК РФ: Незаконные приобретение, хранение, перевозка, изготовление, переработка наркотических средств, психотропных веществ или их аналогов",
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
            GAME_1.points[0] = 0                        # Обнуление очков первого игрока
            GAME_1.points[1] = 0                        # Обнуление очков второго игрока
            GAME_1.Whose_throw = 0                      # Обнуление номера бросавшего            
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
            
            await ctx.send(f'{GAME_1 .players[1]} трусливо сбегает из поединка\nПобеда автоматически присуждается {GAME_1 .players[0]}')
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
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} ваше итоговое значение: {GAME_1.points[GAME_1.Whose_throw]}')
            GAME_1.Whose_throw += 1
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} ваша очедерь. Чтобы совершить бросок напишите -Throw')
        elif  GAME_1.Whose_throw == 1 and ctx.message.author.mention == GAME_1.players[GAME_1.Whose_throw]:
            for number in [0, 1, 2]:
                Toss = random.randint(1, 6)
                GAME_1.points[GAME_1.Whose_throw] += Toss
                await ctx.send(f'{Cube[Toss]}')
            await ctx.send(f'{GAME_1.players[GAME_1.Whose_throw]} ваше итоговое значение: {GAME_1.points[GAME_1.Whose_throw]}')
            GAME_1.Whose_throw = 0
            if GAME_1.points[0] > GAME_1.points[1]:
                await ctx.send(f'{GAME_1.players[0]} одержал победу, поздравьте победителя!')
            elif GAME_1.points[0] < GAME_1.points[1]:
                await ctx.send(f'{GAME_1.players[1]} одержал победу, поздравьте победителя!')
            else:
                await ctx.send(f'Получается ничья. Сыграем ещё?)\nДля начала новой игры напишите "-Roll_play" "Имя_противника"')

            GAME_1.Is_playing = False                   # Завершение игры
            Event = 0                                   # Сброс номера ивента
        else:
            await ctx.send(f'{ctx.message.author.mention} не ваша очедерь.')
    else:
        await ctx.send(f'Нет активной игры')

            

@bot.command() # указываем боту на то, что это его команда
async def naxuy(ctx):
    Url_1 = discord.Embed(
        title="Добро пожаловать!",
        description="Пройдите пожалйста нахуй",
        url='https://rt.pornhub.com',
    )
    await ctx.send(embed=Url_1)


@bot.command()                                          # указываем боту на то, что это его команда
async def Yandex_login(ctx, login, password):           # Логинимся в свой аккаунт Яндекса
    print(f' Пользователь: {login}\n Пароль: {password}\n')
    client = Client.from_credentials('DS-BOT-CHILL@yandex.com', 'Aral7472')
    await ctx.message.delete()                          # Удаление запроса пользователя (чтобы не палить личные данные данные)


@bot.command()
async def join(ctx):

    if ctx.message.author.voice == None:
        Url_1 = discord.Embed(
            title = "No Voice Channel. You need to be in a voice channel to use this command!"
        )
        await ctx.send(embed=Url_1)
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()



@bot.command()
async def play(ctx, arg):           # not work

    if ctx.message.author.voice == None:
        Url_1 = discord.Embed(
            title = "No Voice Channel. You need to be in a voice channel to use this command!"
        )
        await ctx.send(embed=Url_1)
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="bin/ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
        # vc.play(discord.FFmpegPCMAudio("It`s a TRAP.mp3"))
                
        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()


@bot.command()
async def yt(ctx, URL):

    # Solves a problem I'll explain later
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(URL)
    # voice = utils.get(bot.voice_clients, guild=ctx.guild)

    if not ctx.message.author.voice:
        Url_1 = discord.Embed(
            title = "No Voice Channel. You need to be in a voice channel to use this command!"
        )
        await ctx.send(embed=Url_1)
        return

    channel = ctx.author.voice.channel
    voice = await channel.connect()
    
    # await ctx.send(f"Now playing {info['title']}.")

    voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    voice.is_playing()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


bot.run(TOKEN)
# except Exception as e:
#     print(type(e))