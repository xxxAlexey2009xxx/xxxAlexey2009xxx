#импортируем всё что нам нужно
import json
import disnake
from disnake.ext import commands
import time
import asyncio
import random
from helpfunction import scl
#создаём класс
class Rating(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_rate = ""
        self.t1 = time.time()
        self.last_mess_time = {}
        # файлы в которых хранится действующие кол-во рейтинга, сообщений, и секунд проведённых в канале связи
        with open("data/data.json", "r") as f:
            self.rating = json.load(f)
        with open("data/data_messages.json", "r") as f:
            self.data_messages = json.load(f)
        with open('data/time_data.json', 'r') as f:
            self.data_time = json.load(f)
        self.channel = None
        self.l_channel = None
    # функция выполняется каждый раз когда бот включается

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(1012106016332189747)
        self.l_channel = self.bot.get_channel(951866591446990878)

    # функция выполняющася каждый раз когда человек пишет сообщение
    @commands.Cog.listener()
    async def on_message(self, message):
    #проверка на бота
        if message.author.bot:
            return

        bb = "<@" + str(message.author.id) + ">"
        self.data_messages[bb] += 1
        #анти спам
        if bb in self.last_mess_time:
            last_mes_time = self.last_mess_time[bb]
            cur_time = time.time()
            time_dif = cur_time - last_mes_time

            if time_dif < 0.8:
                await message.channel.send("Не спамь!")
                await message.delete()
                # исключаем каналы в котрорых можно спамить
                channels_to_mute = [channel
                                    for channel in message.guild.channels
                                    if channel.type == disnake.ChannelType.text and channel.name not in
                                    ["правила", "for-tests"]]

                for channel in channels_to_mute:
                    await channel.set_permissions(message.author, send_messages=False, reason="Спам")

                await asyncio.sleep(60)

                for channel in channels_to_mute:
                    await channel.set_permissions(message.author, send_messages=True, reason="Конец мута")

        self.last_mess_time[bb] = time.time()

        if self.data_messages[bb] % 50 == 0:
            self.rating[bb] += 5
            await message.reply(f"""{bb}, поздравляю тебя, ты уже написал целых {self.data_messages[bb]}"
                                 сообщени{scl(self.data_messages[bb], 'е', 'я', 'й')}, 
                                 за это я награжу тебя. Продолжай в том же духе!""")
            await message.reply(f"{bb} получил +5 рейтинга за свою активность!")
            if self.rating[bb] == 100:
                await message.reply(file=disnake.File("imgs/catwoman.jpg"))
            else:
                await message.reply(file=disnake.File("imgs/5soc.jpg"))
            # записываем изминения в файлы
            with open('data/data_messages.json', 'w') as k:
                json.dump(self.data_messages, k, indent=4)

            with open('data/data.json', 'w') as f:
                json.dump(self.rating, f, indent=4)

    # функция которая показывет рейтинг на сервере
    @commands.slash_command(description="Показывает социальный рейтинг участников сервера")
    async def rate(self, inter):
        for key in self.rating:
            self.all_rate += " " + key + " - " + str(self.rating[key]) + "\n"
        embed_rating = disnake.Embed(
            title="Вот рейтинг на сегодня:",
            description=self.all_rate,
            color=0xffcdd0
        )
        await inter.send(embed=embed_rating)
        self.all_rate = ""

    @commands.slash_command(description="Узнай, сколько ты насидел")
    async def mytime(self, inter):
        id = f'<@{str(inter.author.id)}>'
        await inter.send(f"У тебя {self.data_time[id]} секунд{scl(self.data_time[id], 'а', 'ы', '')}")

    @commands.slash_command(description="Узнай, сколько ты настрочил")
    async def mymessages(self, inter):
        bb = "<@" + str(inter.author.id) + ">"
        await inter.send(f"У тебя {self.data_messages[bb]} сообщени{scl(self.data_messages[bb], 'е', 'я','й')}")

    @commands.slash_command(description="изменяет рейтинг")
    async def change_rate(self, inter, mention, number):
        self.social_plus = ['imgs/pudge.jpg', 'imgs/rf.jpg', 'imgs/social.jpg', 'imgs/social2.jpg', 'imgs/social_prima.jpg',
                       'imgs/social_valve.jpg']
        self.social_minus = ['imgs/minus_social.png', 'imgs/minus_social2.jpg', 'imgs/social3.png', 'imgs/social4.png']
        embed_ret = disnake.Embed(
            title="изменение рейтинга",
            description=f'у {mention} рейтинг {self.rating[mention] + int(number)}',
            color=0xffffff

        )
        if int(number) > 0:
            embed_ret.set_image(file=disnake.File(random.choice(self.social_plus)))
        elif int(number) < 0 and self.rating[mention] - int(number) < 0:
            embed_ret.set_image(file=disnake.File(random.choice(self.social_minus)))
        else:
            embed_ret.set_image(file=disnake.File("imgs/social.jpg"))
        self.rating[mention] += int(number)

        with open('data/data.json', 'w') as f:
            json.dump(self.rating, f, indent=4)
        await inter.send(embed=embed_ret)
        return f'у Вас рейтинг {self.rating[mention] + int(number)}'
    #функция вызывающася каждый раз когда человек меняет свой статус в канале
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # проверка на бота
        if member.bot:
            return
        #смотрим сколь времяни человек проводит в канале
        async def move_to_channel(destination_channel):
            try:
                await member.move_to(channel=destination_channel)
            except Exception as e:
                print(f"Failed to move member to channel: {e}")

        if after.self_deaf and after.channel:  # Проверяем, находится ли участник в голосовом канале
            await move_to_channel(self.channel)
            print(self.channel)
            self.t3 = time.time()

        if before.self_deaf and before.channel:  # Проверяем, находится ли участник в голосовом канале
            self.t4 = time.time()
            self.data_time[member.mention] -= self.t4 - self.t3

        if not after.self_deaf and after.channel:  # Проверяем, находится ли участник в голосовом канале
            await move_to_channel(self.l_channel)


        if before.channel is None and after.channel is not None:
            self.t1 = time.time()
        elif before.channel is not None and after.channel is None:
            t2 = time.time()
            self.data_time[member.mention] += t2 - self.t1
            if self.data_time[member.mention] >= 86400:
                self.data_time[member.mention] -= 86400
                self.rating[member.mention] += 2

        with open('data/time_data.json', 'w') as f:
            json.dump(self.data_time, f, indent=4)
        with open('data/data.json', 'w') as f:
            json.dump(self.rating, f, indent=4)





def setup(bot):
    bot.add_cog(Rating(bot))
