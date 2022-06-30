import os
import sys
import json
import youtube_dl
import telepotpro
from random import randint
from multiprocessing import Process
from youtubesearchpython import SearchVideos


bot = telepotpro.Bot("5376970460:AAFxRj01upSbnXPg-fqkj2KLtrEomKJeDSM")

def startMsg(chat_id, first_name):
	bot.sendMessage(chat_id, 'Hey, 💓'+ first_name +'💓\n'
	'I am a Music Downloader bot\n'
        '*My* _commands available are_\n'
	'*/song* _song name_ or\n'
	'*/song* _musician name - song name_\n\n'
	'And I will try my best to get your music \n'
        '🎶🎶🎶🎶🎶🎶🎶', parse_mode= 'Markdown')

def errorMsg(chat_id, error_type):
	if error_type == 'too_long':
		bot.sendMessage(chat_id, 'Sorry! The video too is long to convert!\n'
			'Order something 30 minutes or less.', parse_mode= 'Markdown')

	if error_type == 'spotify_command':
		bot.sendMessage(chat_id, '😬 \nThe bot does not support Spotify links', parse_mode= 'Markdown')

	if error_type == 'invalid_command':
		bot.sendMessage(chat_id, '‼️ *I did not understand 🤔! *\n'
			'My commands are:\n'
                        '*/song* _song name_\n'
			'*/song* _musician name song name_', parse_mode= 'Markdown')

def downloadMusic(file_name, link):
	ydl_opts = {
		'outtmpl': './'+file_name,
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '256',
		}],
		'prefer_ffmpeg': True
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info_dict = ydl.extract_info(link, download=True)

def validMusicInput(userInput, chat_id, chat_type):
		#Search music on youtube
		search = SearchVideos(userInput[5:], offset = 1, mode = "json", max_results = 1)
		resultados = json.loads(search.result())
		
		#Get video duration
		duration = resultados['search_result'][0]['duration'].split(':')
		splitCount = len(duration)

		if int(duration[0]) < 30 and splitCount < 3:
			title = resultados['search_result'][0]['title']
			link = resultados['search_result'][0]['link']
			file_name = title +' - '+str(randint(0,999999))+'.mp3'

			bot.sendMessage(chat_id,' Name of Song\n'+'⏬⏬⏬⏬⏬⏬⏬⏬⏬⏬\n'+title+'\n'+'🔗 '+link+' 🔗')
			DownloadingMsg = bot.sendMessage(chat_id,' 🔻 Downloading🔻 '
				'\n_📛Please wait till I download it📛_', parse_mode= 'Markdown')
                      
			#Download the music
			downloadMusic(file_name, link)

			bot.sendAudio(chat_id,audio=open(file_name,'rb'))
			bot.deleteMessage((chat_id, DownloadingMsg['message_id']))
			bot.sendMessage(chat_id, '✅Successfully Uploaded✅')

			print ("Sucess!")
			os.remove(file_name)

		else:
			errorMsg(chat_id, 'too_long')

		pass

def recebendoMsg(msg):
	userInput = msg['text']
	chat_id = msg['chat']['id']
	first_name = msg['from']['first_name']
	chat_type = msg['chat']['type']

	if chat_type == 'group':
		if '@yourfavmusicbot' in userInput:
			userInput = userInput.replace('@yourfavmusicbot', '')

	if userInput.startswith('/start'):
		#Shows start dialog
		startMsg(chat_id, first_name)

	elif userInput.startswith('/music') and userInput[5:]!='':
		if 'open.spotify.com' in userInput[5:]:
			errorMsg(chat_id, 'spotify_command')

		else:
			#Process the music
			validMusicInput(userInput, chat_id, chat_type)

	else:
		#Invalid command
		errorMsg(chat_id, 'invalid_command')

	pass

def main(msg):
	main_process = Process(target=recebendoMsg, args=(msg,))
	main_process.start()

bot.message_loop(main, run_forever=True)
