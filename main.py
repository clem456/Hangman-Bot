import nextcord
from nextcord.ext import commands
config = json.load(open("config.json", encoding="utf-8"))


bot = commands.Bot(
	command_prefix="_", 
)

@bot.event
async def on_ready():
	x = datetime.datetime.now()
	print(f'Logged in ' + str(x))
	print("Username: ", bot.user.name)
	print("User ID: ", bot.user.id)

@bot.command()
async def checkcpu(ctx):
	cpu_per = round(psutil.cpu_percent(),1)
	mem = psutil.virtual_memory()
	mem_per = round(psutil.virtual_memory().percent,1)
	msg = "RAM is " + str(mem_per) + "%"
	msg += "\nCPU is " + str(cpu_per) + "%"

	await ctx.message.edit(msg)  
  
  
if __name__ == "__main__":
  bot.run(config["token"])
