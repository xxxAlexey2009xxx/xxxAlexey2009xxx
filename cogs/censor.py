from disnake.ext import commands


# создаём класс наследник
class Censor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/ban_words", 'r') as f:
            self.censored_words = f.read()  # список бан слов
            self.censored_words = self.censored_words.split()
# функция которая проверяет каждое сообщение
    @commands.Cog.listener()
    async def on_message(self, message):
        for censored_word in self.censored_words:
            if message.content.lower().startswith(censored_word):
                await message.channel.send("Не говори так!")
                break
    @commands.slash_command(description='добавить бан ворд')
    async def add_ban_word(self, word):
        self.censored_words.append(word)
        with open('data/ban_words', 'w') as f:
            f.write(str(self.censored_words))

def setup(bot):
    bot.add_cog(Censor(bot))
