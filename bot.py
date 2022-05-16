import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(name)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("Dejavu Tag Bot, Qurup'larda User Tag Üçün Yaradıldım.\n\nƏtraflı Məlumat Üçün/help'i Toxuna Bilərsən.",
                    buttons=(
                      [Button.url('➕ Məni Qurupa Sal ➕', 'https://t.me/DejavuTaggerBot?startgroup=a'),
                      Button.url('📣 Qurup', 'https://t.me/DejavuGurup'),
                      Button.url('🚀 Kanal', 'https://t.me/DejavuSupport')]

                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "Loungetagger bot'un Yardım Menüsü\n\nKomut: /all \n  Bu komutu, başkalarına bahsetmek istediğiniz metinle birlikte kullanabilirsiniz. \nÖrnek: /all Günaydın!  \nBu komutu yanıt olarak kullanabilirsiniz. herhangi bir mesaj Bot, yanıtlanan iletiye kullanıcıları etiketleyecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/loungetaggerbot?startgroup=a'),
                      Button.url('📣 Support', 'https://t.me/loungesupport'),
                      Button.url('🚀 Sahibim', 'https://t.me/bodrumlubebekk')]
                      Button.url('💻 Sahib', 'https://t.me/MUCVE_M')] 
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond(" Bu Əmir Qurup'larda İstifadə Edə Bilərsiniz.!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Ancaq Yöneticiler hamısını Tag Edə Bilərəm.!")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Əvvəlki Mesajla Userləri Tag Edə Bilərəm.! (gruba eklemeden önce gönderilen mesajlar)")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Mesaj Əlavə Edin.!")
  else:
    return await event.respond("Bir Mesajı Yanıtlayın veya Mesaj Əlavə Edin.!")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tag Dayandırıldı.!")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.res
