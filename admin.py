#third version
#created by Griffin Baird
#  2018-03-14
# discord bot named 'tactical command

#imports discord related elements
import discord							#discord module
from discord.ext.commands import Bot	#gets the bot module 
from discord.ext import commands		#gets the command module
bot = commands.Bot(command_prefix = "!")#commands start with !

#discord related elements, keep the token a secret
token = "INSERT_TOKEN_HERE"


#event handler & time handler & os for file navigation
import asyncio	#discord.py 1.16
import time		#for logging time is used
import os		#for directory navigation and file upload

bot.remove_command('help')#removes default command for help, allows for override 
sys_flag = 0 #a flag to determine a set a behaviors (roles, exiting, uploading)
			 #0 default settings 		(some functions not available)
			 #1 exiting					(manipulates log book and stops further log book stamping)
			 #2 administrator access	(all functions available)
			 #3 error 					(program starts to log a lot more information for debugging)
			 
#When the bot is ready to receive input
@bot.event
async def on_ready():
	print("Bot is ready!")
	#await bot.edit_profile(password=None, username = "Blue Garden")
	os.chdir("src")
	print("inside the source folder")
	print("\t".join(os.listdir())) #error checking directory (shows all files)
	log("\n\n operational @ " +getNow()+ "\n" )#posts timestamp to logbook

#lists all commands
@bot.command()
async def help():
	print("asked for help")	
	await bot.say("This is an administrator bot for tactical games, keep in mind, that this bot keeps chat logs with your username \n commands are as follows "+
				"\n !read_logs 					   			    						  #uploads the log file"+
				"\n !files 					   			    						      #displays all files in the source folder"+
				"\n !upload_file filename 	   			    		 	        #sends a file given a name and id"+
				"\n !create_role rolename											#creates a role with a particular name"+
				"\n !delete_role rolename											#deletes a specific role given the name"+
				"\n !display_roles												           #displays all current roles"+
				"\n !add_role rolename 			   			    				 #gives you a valid role"+
				"\n !remove_role rolename 					   		 		 #removes one of your roles"+
				"\n !shut_down code						        						 #logs off bot")

#shuts down the bot
@bot.command()
async def shut_down(*code):
	if(code[0] == '1877'):
		await bot.say('Order recieved, shutting down')
		await bot.logout()
	else:
		await bot.say('invalid authority')

#displays all the files in the source folder	
@bot.command()
async def files():
	await bot.say('`'+'` `'.join(os.listdir()) + '`')

#read_logs	(uploads log (txt format))
@bot.command(pass_context=True)
async def read_logs(ctx):
	await bot.send_file( ctx.message.channel,"logs.txt")

	
#send secret document to user
@bot.command(pass_context=True)
async def dive(ctx,fileName):
	try:
		os.chdir('-')
		await bot.say("Dive complete...")
		await bot.send_file( ctx.message.channel, ""+fileName)
		os.chdir('..')
	except Exception as e:
		os.chdir('..');
		await bot.say("ERROR " + str(e))
		
#upload_file (from the source folder)
@bot.command(pass_context=True)
async def upload_file(ctx,fileName):
	try:
		await bot.send_file( ctx.message.channel, ""+fileName)
	except Exception as e:
		await bot.say("Error "  + str(e))
		

#create_role add in keyword arguments
@bot.command(pass_context = True)
async def create_role(ctx, rolename):
	try:
		await bot.create_role(ctx.message.server,name = rolename)
	except Exception as e:
		await bot.say("Error " + str(e))
		

#delete_role (as long as it exists)
@bot.command(pass_context = True)
async def delete_role(ctx, rolename):
	try:
		role = discord.utils.get(ctx.message.server.roles, name=rolename)#finds the role
		await bot.delete_role(ctx.message.server,role) #deletes the role
	except Exception as e:
		await bot.say("Error " + str(e))

#display_roles
@bot.command(pass_context = True)
async def display_roles(ctx):
	roles = ctx.message.server.role_hierarchy#gets all the roles
	list_roles = "\n"#creates a string to store them in
	
	i = 0
	for i in range(0,len(roles)-1):#goes through all roles except for everyone
		#print(i)
		list_roles += roles[i].name+ " \n"#adds role to list
	#print(list_roles)	
	await bot.say(list_roles)

#add_role to the user who requests it
@bot.command(pass_context = True)
async def add_role(ctx,rolename):
	role = discord.utils.get(ctx.message.server.roles, name=rolename)#finds the role
	if(str(role) == "None"):#if the role does not exist
		print("INVALID ROLE REQUEST")
		await bot.say(" the role you requested does not exist")
	else:
		try:
			await bot.add_roles(ctx.message.author, role)#assigns the role
		except Exception as e:
				await bot.send_message(ctxmessage.channel, "You cannot have that role " +str(e))
				await bot.say("You cannot have that role " + str(e))

#remove_role to the user who requests it
@bot.command(pass_context = True)
async def remove_role(ctx,rolename):
	role = discord.utils.get(ctx.message.server.roles, name=rolename)#finds the role
	print(role)
	if(str(role) == "None"):#if the role does not exist
		await bot.say(" this role does not exist")
	
				
	else:
		try:
			await bot.remove_roles(ctx.message.author, role)#removes the role
		except Exception as e:
			await bot.say( "You cannot remove that role " +str(e))
			print ("You cannot remove that role " +str(e) )

#bot can talk (interupts function listener)
@bot.command(pass_context = True)
async def talking(ctx):
		x = ""
		while x != "im done":
			x = input("Give me words of strategy\n")
			await bot.say(x)
			time.sleep(1)
		
@bot.command(pass_context = True)
async def fuckoff(ctx):
	await bot.say("Take a powertrip somewhere else")
		
#catches errors & logs result
@bot.event
async def on_command_error(ctx, error):
	print("Invalid commmand \t ")
	await bot.send_message(error.message.channel,"Command does not exist ")
	log(":ERROR")
				
#on message logs info
@bot.event
async def on_message(message):
	log( message.content + "     from    " + message.author.name)
	#allows commands to be proccessed after message
	await bot.process_commands(message) #after on message, checks for command handler

#time getting function
def getNow():
	cTime = time.strftime("%Y/%m/%d %H:%M")#time format
	return cTime	

#logging function
def log(str):
	file = open("logs.txt", "a")#opens stream with append
	file.write("\n "+getNow()+"\t" +str+ "\n" )#enters message info and gives it a time stamp
	file.close()#closes stream

#runs the bot
bot.run(token)