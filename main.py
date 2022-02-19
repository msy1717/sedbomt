import os
import logging
from replit import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup,KeyboardButton,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,MessageHandler,Filters
from aiotube import Search, Video, Channel, Playlist, Extras
import tweepy
from airdrop import airdrop
from web3 import Web3, eth
from server import keepalive
keepalive()


x=[]


# twitter auth
# assign the values accordingly
consumer_key = os.environ['cid']
consumer_secret =os.environ['csecret']
access_token =os.environ['at']
access_token_secret =os.environ['atsecret']

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

user = api.get_user(screen_name='developermano')
print(user.followers_count)

del db['eth']
del db['claimed']

db['eth']=[]
db['claimed']=[]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

my_secret = '5006517849:AAE6ySviKReO-NaR55IEDmbCF-WxxDf_4Dc'
bot=Bot(my_secret)



def claimtoken(ethad,chatid):
  print(ethad)
  airdrop(ethad)
  bot.send_message(chatid,"token is claimed")
  






def groupid(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(update.message.chat_id)





def start(update: Update, context: CallbackContext) -> None:    
    keyboard = [
        [
            InlineKeyboardButton("join telegram group",url=os.environ['telegramgroupurl']),
            InlineKeyboardButton("joined",callback_data='telegramgroup')
        
        ]    
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('''
🙏 welcome to airdrop bot. i will give a task .if do , i can claim the token
 1.follow my telegram channel.
  ''',reply_markup=reply_markup)




def ethaddress(update: Update, context: CallbackContext) -> None:
  if update.message.chat_id > 0: 
    if update.message.chat_id in db['eth']:
      if not Web3.isAddress(update.message.text):
        bot.send_message(update.message.chat_id,"it is not eth address")
        return True
      x=db['eth']
      x.remove(update.message.chat_id)
      cl=db['claimed']
      if not update.message.chat_id in cl:
        cl.append(update.message.chat_id)
        claimtoken(update.message.text,update.message.chat_id)
    else:
      bot.send_message(update.message.chat_id,"you are already claimed the token")






def callback(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()

    if query.data=="claim":
      bot.send_message(update.callback_query.message.chat_id,text=" send your wallet address .")
      x=db['eth']
      x.append(update.callback_query.message.chat_id)
      print(x)


    if query.data=="twitter":
      print(update.callback_query.message.chat_id)
      user = api.get_user(os.environ['twitterid'])
      if user.followers_count > db["twitterfollow"]:
        query.edit_message_text(text="thank you for joined my twitter handle . claim your token now")

        keyboard = [
        [
            InlineKeyboardButton("claim 🍹",callback_data='claim')       
        ]    
    ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(update.callback_query.message.chat_id,text="you have complete all task .",reply_markup=reply_markup)


    if query.data=="youtube":
      print(update.callback_query.message.chat_id)
      channelid = os.environ['channelid']
      chan = Channel(channelid)
      if chan.subscribers > db['youtubesub']:
        query.edit_message_text(text="thank you for joined my youtube channel . go to your next task")

        keyboard = [
        [
            InlineKeyboardButton("follow on twitter",url=os.environ['twitterurl']),
            InlineKeyboardButton("joined",callback_data='twitter')       
        ]    
    ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(update.callback_query.message.chat_id,text="2. start your second task. \n follow my twitter handle",reply_markup=reply_markup)
        user = api.get_user(screen_name=os.environ['twitterid'])
        db["twitterfollow"]=user.followers_count


    if query.data=="telegramgroup":
      print(update.callback_query.message.chat_id)
      s=bot.get_chat_member(int(os.environ['telegramchatid']),update.callback_query.message.chat_id)

      if s.status =='member':
        query.edit_message_text(text="thank you for joined my group. go to your next task")
        keyboard = [
        [
            InlineKeyboardButton("follow on youtube",url=os.environ['youtubeurl']),
            InlineKeyboardButton("joined",callback_data='youtube')       
        ]    
    ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(update.callback_query.message.chat_id,text="2. start your second task. \n follow my youtube channel. ",reply_markup=reply_markup)
        channelid = os.environ['channelid']
        chan = Channel(channelid)
        print(chan.subscribers)
        db["youtubesub"]=chan.subscribers
      else:
        bot.send_message(update.callback_query.message.chat_id,"sorry , i couldn't find you.")




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    token=os.environ['token']
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('groupid', groupid))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, ethaddress))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
