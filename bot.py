import sys
import time
import telepot
import requests

from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from pprint import pprint

imgflip_login = "levstestbot"
base_url = 'https://api.imgflip.com/'

# keep track of received messages
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, 'Fuck you, ' + msg['chat']['first_name'])
    pprint(msg)

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        meme_parts = query_string.split(':')

        meme_id = keymap[(meme_parts[0].lower()).replace(" ", "")]

        meme_text = meme_parts[1].split('@')

        if len(meme_text) < 2:
        	meme_text.append("")

        articles = []

        if meme_id:

        	payload = {'template_id' : meme_id,
        	'username' : imgflip_login, 'password' : imgflip_login,
        	'text0': meme_text[0], 'text1' : meme_text[1]}

        	r = requests.post(base_url+'caption_image', data = payload)

        	# print r.text

        	r = r.json()
        	if r['success']:
        		url =  r["data"]["url"].replace("\\","")

        		# print url

        		articles = [InlineQueryResultPhoto(
                        id='abc',
                        title=query_string,
                        photo_url = url, 
                        type = 'photo',
                        thumb_url = url, 
                        photo_width = 100,
                        photo_height = 100
                   )]

        return articles

    answerer.answer(msg, compute)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    pprint(msg)
    print ('Chosen Inline Result:', result_id, from_id, query_string)

TOKEN = sys.argv[1] 

bot = telepot.Bot(TOKEN)
# print bot.getMe()

# res = bot.getUpdates()

# bot.message_loop(handle)

# Requested all the memeses to rule them all
memes = requests.get(base_url+'get_memes')

keymap = {}

memes = memes.json()

for meme in memes['data']['memes']:
	name = meme['name'].lower()
	keymap[name.replace(" ", "")] = meme['id']

keymap['megusta'] = 7249133

# print memes.text

answerer = telepot.helper.Answerer(bot)

bot.message_loop({'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result},
                 run_forever='Listening ...')

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)