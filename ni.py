import random
import asyncio
from telethon import TelegramClient, events, Button
from datetime import datetime, timedelta

# API credentials from https://my.telegram.org/
API_ID = '21259513'
API_HASH = '29e43fc190ebaef2ee94542cafb0614d'
BOT_TOKEN = '7842463023:AAF3oPkNW3D_X9KIXazBfP98qE2sdYt7vRk'

#Admins 
ADMIN_USERNAME = "Seiao"

# Admins' Telegram user IDs
ADMIN_IDS = [6076683960, 5767166269, 6241590270]  # Replace with actual admin IDs
approved_users = {}  # Store approved users with expiry time
welcome_targets = {}  # Store the target users for auto-replies in each group
welcome_activators = {}  # Track who activated the welcome replies
group_admin_requests = set()  # To track the groups where the bot has already sent the "admin" request message
muted_users = {}  # Store muted users for each group

broadcasting = False
waiting_for_broadcast_message = None
broadcast_message_content = None
active_users = set()  # Store active users for broadcasting

WELCOME_MESSAGES = [
    "Chup teri maa ki chut ;(",
    "Jana jhaatu teri maaki chut chaatu ✓",
    "Kaapta hai kutta thand me, or teri mummy ko khushi milti bs mere lund me",
    "@PythonBotz ka Python Teri gand me dal dunga",
    "Sasti naali ke keede chup",
    "Tmkc me gandhi ji ki lathi",
    "Tere muh me hag dunga •_•",
    "Chup kutiya ke bachhe",
    "teri maa randi",
    "Beta Chup cahp @PythonBotz Join kar le nhi to teri gand me loda dal dunga",
    "teri behan dhandhe wali",
    "Tera baap hizda",
    "Randi ke bachhe",
    "Bhenchod baap se panga matt le Warna maa chodh di Jayegi 🤬",
    "madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye",
    "TERA BAAP JOHNY SINS CIRCUS KAY BHOSDE JOKER KI CHIDAAS 14 LUND KI DHAAR TERI MUMMY KI CHUT MAI 200 INCH KA LUND",
    "teri ma Randi tera baap hizda kaali gaand kay Khade baal jhaatu Randi kay chodu",
    "teri mummy q xhudi?",
    "gb road ki paidaish hai tu",
    "or kitna chudega?",
    "Chuda q?",
    "Tu or teri mummy mere lwde pe",
    "Kutta hai tu kutta (or teri mummy kutiya",
    "हिंदी की मात्रा बनाते हुए तेरी दीदी पेल दूंगा चमार की औलाद 🤭🤣",
        "Tu yaha typing kar rha or idhar teri mummy chud rahi chutiye💀",
        "Jhaat se baandhkr teri mummy ko faasi laga dunga randi ke😂😎",
        "@PythonBotz ke bot se tu chud rha yad rakh",
        "Aisa lund fek ke marunga ki tera khandan chud jayega hizde ki paidaish 👹🙈",
        "Abe chamar teri mummy ko 🪑कुर्सी pe bitha ke इमरान हाशमी wala scene re-create kar dunga💀🤣",
        "Chup chhoti jaat ke !! Bhosdike teri awkaat ni hai av mere saamne bolne ki अछूत 🖕🏻🗣️",
        "Main yaha imagine karunga or waha teri behan pregnant ho jayegi😝🥱",
        "झाटे ना चूची तेरी मम्मी मेरी कुची पूची 😍🥰🙈",
        "ठंडी आ गई ना? तेरी मम्मी के भोसड़े में आग लगाकर अपने हाथ सेक लूंगा🤡",
        "लाइफबॉय का साबुन डव वाले शैंपू में, तेरी मम्मी चुदेगी बेटा चलते हुए टेंपू में⚙️😈️",
        "Muh band rkh 1 dollar me bikne wali ke bete🤫😂",
        "GAND KII DHAAR BHOSDIKE FATEE HUE CONDOM KI NAAJAIS PAIDAISH",
        "Teri maa ki choot gand kay tatto teri maa ka bhosda karke uski gaand mai ping pong kar dunga",
        "madar chod bhosdke esa lagta h apne hii taaate kaat ke chipka diya apni shakal dekh lodee jese shakal aur gand me h aakal",
        "Teri ma ki gand me hathi ka lund dalke asa chodunga Na Bacha hojayega Johny sins ,ke lund se chudwaungu bhosdike",
        "GAND MAI VIMAL KI GOLI BNA KAR DE DUNGA BHENCHO TERI GAAND MAI RAILWAY STATION KA FATAK DE DUNGA 😂😂🤬🖕",
        "teri maa k bhosde mai MDH CHANA MASALA daal k tere baap ko vo spicy bhosda khila dunga 🥵🤮",
        "maa k lode tere jese randi k baccho ko bachpan mai maar dena chiye",
        "madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye",
        "Bhenchod baap se panga matt le Warna maa chodh di Jayegi 🤬",
        "Abbe teri maa ki chut ko kutte se katva dunga randi k pille 😡😠😤teri behn ki chut mai set top box ghusa dunga mai madarchod 😳 chutmarik teri tatti jesi shakl pe pad dunga bhen k lode chutiye madarchod kitna chutiya aadmi hai Tu😡 jaya bachan bana kai chod dunga teri behn ko😋 maa k lode tere jese randi k baccho ka abortion krva dena chiye 😤 bhosdk teri maa k bhosde mai MDH CHANA MASALA daal k tere baap ko vo spicy bhosda khila dunga 🤢 Tere dalle baap ka lund uth'ta hai nhi tbhi teri maa 150 k bhav se deti hai 😍 madarchod k baache sudhar ja 😡😠😤",
        "ABA SUN ☀ CHOR BHOSDI TERI MAA KO 🤶 NANGHI KR 🆎 KA 🔫 LUNDO KI 🆖🤴🅱 MALA PAHNAKA CHAURAHA KASAO CHAKKAR MARVAUNGA JHAAT KA 🔫 MARA 🍑🅰 CHILLAR SALA TERI BHN KI 🆖🤴 CHOOT. BAHOT BADBUDAR THI 🅱🍑 FIKR MAT 😱 KR 🆎 AB 😩 SAHI HO 🎅🏻 JAYAGI KYOKI MAINA USKI BADBUDAR CHOOT TEZAAB SA 🅱 SAAF KR 🆎 DIYA HAI 👋 MAA KA 🔫 LAUDAAAJ TERI BHN CHOD CHOD KAITNA KHOON NIKALUGA KI 🆖🤴 USSA EK 🅰♌ MAKAN PUTH JAYAGA©LUND KA 🚀 KHAJOOR SADA ANGOOR DIKHNA MAI 💌 LANGOOR.BHOSDA CHOD TERI MAA KABADA BADA 😈🍑 THAN KAT 🍦🍪🤑 KA 🚀 TERA 👉 GHAR COURIER 📯 KAR DUGA FIRAPNA RANDUA BAAPKA SATH BAITHKA KA 🔫 USSA FEWIKWICK SA.FIX KARNA AGAR TUM DONO.GANDUO NA ✊ USSA FIX ⚙🔧 KARLIYATO ZADA KHUSH MAT 😱 HONAKYOKI USKA BAAD TERI BHNWALA COURIER 📯 AA ⚡ JAYAGAABA CIRCUS 🎪🤡 SA 🅱 BHAGA JANWAR LODUMAL KI 🆖🤴🅱 GANDMAL AULAD JITNI TERI UMAR NAHI 🎉🔹 HOGI UTNA LADKO KI 🆖🤴 MAINA GANDMARA HAI 🤓 TU 2️⃣ APNA BAAP 👨👶 KO 🤶 CHODNA SIKHAYGA",
        "Tu ye bata main teri mummy ko bade para graph se chodu ya chhoti shayari se?😂",
        "Teri mummy ki sakal mere gali ke ek kutiya se milti hai️",
        "Bhosadchod Teri mayya ki gaand me Teri bahan ko le ghuskar itne bache paida karunga ki tujhe ye decide karte karte heart attack a jayega ki tu unka mama hai ya bhayya",
        "TARI MAA KO CHOD KA 9MONTH BAAD EK OUR RAAVAN NIKALGA BHAN KA LODO SAMBAL KA RAHNA BAAP SA MAA CHOD DAGA JIS NA BHI FAADA KIYA MUJSA..# 🤧😡🤬",
        "Teri mummy se puch suhagrat me usko setisfaction kisne diya tha, q ki tera baap to 6kka tha",
        "Chhipkali jaise deewal pe chadh ke teri mummy ke muh me moot dunga.",
        "Teri mummy jab nahate rahegi to bathroom ke neeche se usko nangi dekh lunga🌟",
        "Teri mummy ko nahane ka to saukh hoga hi na?? moot kar naha du kya?😂",
        "Teri behan ki saare jhaate प्लास se ukhaad dunga🐚🐌",
        "Teri mummy ko itna chodunga ki 7 din tak weakness rhega use😼😹",
        "Teri mummy ki gaand me 10 rupay wali nakli gaadi ghusa dunga💀 q ki usse jyada uski aukat nahi😂🤣",
        "Jaakr hospital me apna DNA check karwa, doctor v terko RJ ka beta btaayenge🗣️👥",
        "Teri mummy ki chut pe daant se kaat kar khoon baha dunga 🩸🌷",
        "Behan ke lwde teri mummy din me 10 customer dhundhte hue rehti hai or tu uske dhandhe wale kamaye paise se yaha online badmosh ban rha chutiye🤣",
        "Tu apni behan ko smjha randi ke pehle kahi wo v teri mummy ki tarah professional randi na ban jaaye💀",
        "Tere or tere jaiso ki rupay dekar roj mummy chodta hu gareeb",
        "Bank lootkar uske rupay se teri mummy khareed lunga🤑️",
        "Teri mummy ko itna chodunga ki wo 2 month hospital me admit rhegi🙊☠️",
        "Abe raand ke bchhe tu bolega bhosdike teri mummy ko smjha na ghar ghar jaakr chudti rehti hai saali",
        "jungle me chhor kar teri mummy ki sher se chudwa dunga randi ke",
        "काली घाटी के अंधेरे में तेरी मम्मी चोद कर भाग जाऊंगा🥱😝",
        "Teri behan ko itna pelunga ki agle hi din se usko randi banne ka saukh chadh jayega🥵",
        "Rocket ki speed se teri mummy ki gand me lund ghusa dunga bhosdi ke",
        "ek din me 9 round chod dunga teri mummy ko",
        "chup reh warna teri behan ke sath shower together le lunga",
        "teri mummy ki chut me gulab ke kaante daal dunga madarchod",
        "or kitne chudega randi ke sharam kar tere itna to teri mummy v nahi chudti",
        "Jhaatu",
        "Chamar",
        "randike",
        "Tujhe pta hai teri behan bhi teri mummy ki tarah randi ban rhi🤭😮‍💨",
        "q teri maa randipanti chhor ke sudharna chahti hai?, mere lund pe bitha pehle💀💞",
        "Sun? Teri maa rand ki sardarni otey¿?🤗",
        "Teri mummy ke boobs dabau ya chut khau?😘",
        "teri mummy ki chut ki seal toot gyi kya?😁",
        "Randike chup ho jaa",
        "Achha? oohhohoho? Chup teri maaki chut",
        " Hatt bhosdiwale",
        "Ger ger ke marunga",
        "patak patak ke chodunga teri didi ko",
        "Sadi hi chut wali ke bete",
        "Teri mummy ki chut me bidi fook dunga",
        "Jhaate saaf kr du kya teri mummy ke?",
        "Kutte se chudwa dunga teri behan ko",
        "सस्ती रण्डी के बच्चे",
        "kutte ki paidaish",
        "Chup gareeb",
        "Tere baap 6kka tha isilye ye proof hai ki tu mera hi beta hai",
        "kaali ghaati ke andhere me teri mummy pelkar bhaag jaunga",
        "Ghar ghar me shor hai teri mummy ki chut kamjor hai, kabhi bhi fatt skti hai💀",
        "Gang rape krwa du kya teri mummy ka?",
        "Sun tujhe pta hai teri behan kitno se chudi hai¿?",
        "Kutte ka lund or teri mummy ki chut",
        "Apne ghar ki saaf safai krwa lunga teri mummy se",
        "Teri bua ki jhuka kr gand maar lunga",
        "aisa lund fek ke marunga kibteri puri khandan chud jaegi",
        "Tu mera hi beta hai chutiye",
        "Teri mummy ki kaali gand",
        "teri budhi bua ki safed chut ki baal",
        "Jhate saaf krwaunga teri behan se apne",
        "teri mummy ki gand me mera smily emoji",
        "mera mental health teri mummy ki tarah hai, hmesa chudta rehta",
        "teri maa kitno se chudi hai?",
        "jhaat ke baal",
        "gadhe ke bachhe",
        "kutti ke pille",
        "Tere baap ki biwi mere lwde pe",
        "Maja aaya chudkr?",
        "aagya swaad?",
        "Kaisa laga chudkr bete?",
        "Buddhi ke baal",
        "Teri mummy mere bed pr",
        "teri ammy ke jh@nto ko pakad ke building se latka dunga.",
        "Kaali ch00t wali r@nd ke bachhe behnch0d",
        "Paodaan ki shakal ke g@ndu sale.",
        "Vimal khane wale r@ndi ke bachhe m@dharch0d.",
        "TARI MAA KO CHOD KA 9MONTH BAAD EK OUR RAAVAN NIKALGA BHAN KA LODO SAMBAL KA RAHNA BAAP SA MAA CHOD DAGA JIS NA BHI FAADA KIYA MUJSA..# 🤧😡🤬",
        "BHAN KA LODA TARI MAA KO CHOD CHOD KA PAGAL KAR DU BHAN KA DINA TU GALI DAGA MUJAE RANDI KA BAALK HARMI KA CHUDA HUA SATVA NAMUNA TARI BHAN CHOD DUNGA ASA CHODUNGA KI TARI BHAN KI SAAT PUSTA MARA LUND KA VAAR SA PARALISS NIKALNGI SALA TARI BHAN KO ROAD PA LAJA KA KA NANGA KAR KA BAAXHO SA CHUD VAU ।। 🤬🤬🤮🥵",
        "ABA CHOOT KA 🚀 TAPAKTA PANI NANKU MOCHI KI 🆖🤴 LAWARIS AULAD TERI MAA KA 🚀 BHOSDA PHAD KA 🔫 JHAAD PA 👨 TANG 🍋 DUGA MADARBHOSDI AAJ TO CHODUGA TERI AMMA TOD KA 🔫 KHATIYA UKHAD LENA 🎽⚽ BETA 💰 MERI JHAATIYA o_OSAlA SUAR KI 🆖🤴🅱 AKHRI NASAL 👃. TERIBHN KO 🤶 LAMBI LAMbI ROAD 🗾🛣 PE 🍇💉 LAMBA LAMBA DAUDA KA 🔫 LAMBA LAMBA LUND DUGA ABA aPNI MAA KI 🆖🤴 PHATI CHOOT KA 🔫 DIWANA ITNI ZOR SA 🅱 GAND PALAAT MARUGA JIS ⁉❕❔ CHOOT KA 🔫 TU 🤔 DIWANA HAI 🐯 USSI CHUT MAIGHUS JAYAGA...:-[:-);-):-",
        "lwde",
        "Madrchod @PythonBotz Join kar",
        "kaali chut teri mummy ki",
]

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Helper function to check approval
def is_approved(user_id):
    if user_id in approved_users:
        expiry_time = approved_users[user_id]
        if datetime.now() < expiry_time:
            return True, (expiry_time - datetime.now())
    return False, None


# /start command
@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    user_id = event.sender_id
    if user_id in ADMIN_IDS:
        await event.reply("🗿 **Hey Admin**, Welcome Back!")
    elif user_id in approved_users:
        approved, time_left = is_approved(user_id)
        if approved:
            await event.reply(f"✅ You Are Approved.\nTime left: {time_left}.\n\nDev : @PythonBotz")
        else:
            del approved_users[user_id]
            await event.reply("🚫 _Your Approval Has Expired. Contact @Seiao for renewal._")
    else:
        await event.reply("**🚫 You are not Authorized to Use This Bot.\n_Contact @Seiao & @CodeRehan_ for approval.**")
    active_users.add(user_id)


# Approve command
@bot.on(events.NewMessage(pattern='/yele'))
async def approve_command(event):
    if event.sender_id not in ADMIN_IDS:
        await event.reply("🚫 You Are Not Authorized.")
        return

    args = event.message.text.split()
    if len(args) < 3:
        await event.reply("❌ Usage: /yele {user_id} {time} (e.g., 1d, 5h)")
        return

    try:
        user_id = int(args[1])
        duration = args[2]
        time_mapping = {'d': 'days', 'h': 'hours', 'm': 'minutes', 's': 'seconds'}
        time_value = int(duration[:-1])
        time_unit = time_mapping.get(duration[-1])

        if not time_unit:
            raise ValueError

        expiry_time = datetime.now() + timedelta(**{time_unit: time_value})
        approved_users[user_id] = expiry_time
        await event.reply(f"✅ User `{user_id}` Approved for {duration}.")
    except ValueError:
        await event.reply("❌ Invalid time format. Use: 1d, 5h, etc.")


# Unapprove command
@bot.on(events.NewMessage(pattern='/bhag'))
async def unapprove_command(event):
    if event.sender_id not in ADMIN_IDS:
        await event.reply("🚫 You Are Not Authorized.")
        return

    args = event.message.text.split()
    if len(args) < 2:
        await event.reply("❌ Usage: /bhag {user_id}")
        return

    try:
        user_id = int(args[1])
        if user_id in approved_users:
            del approved_users[user_id]
            await event.reply(f"✅ User `{user_id}` Unapproved.")
        else:
            await event.reply("⚠️ User Not Found.")
    except ValueError:
        await event.reply("❌ Invalid User ID.")


# /chudle command
@bot.on(events.NewMessage(pattern='/roo'))
async def welcome_command(event):
    user_id = event.sender_id

    if user_id not in ADMIN_IDS and user_id not in approved_users:
        await event.reply("🚫 You Are Not Authorized. Contact Admin for approval.")
        return

    reply = await event.get_reply_message()
    if reply:
        target_user = reply.sender_id
        chat_id = event.chat_id

        if chat_id not in welcome_targets:
            welcome_targets[chat_id] = set()

        welcome_targets[chat_id].add(target_user)
        welcome_activators[(chat_id, target_user)] = user_id
        await event.reply(f"✅ Auto Replies Activated for `{target_user}`.")
    else:
        await event.reply("❌ Reply to a User or Mention a User ID.")


# Auto-reply
@bot.on(events.NewMessage)
async def auto_reply(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    if chat_id in welcome_targets and sender_id in welcome_targets[chat_id]:
        if sender_id in muted_users.get(chat_id, set()):
            return  # Don't reply if the user is muted
        random_message = random.choice(WELCOME_MESSAGES)
        await event.reply(random_message)
        
        
  ### 🛑 STOP
  
@bot.on(events.NewMessage(pattern='/hehe'))
async def stop_welcome(event):
    user_id = event.sender_id

    # Check if the user is authorized
    if user_id not in ADMIN_IDS and user_id not in approved_users:
        await event.reply(
            "🚫 <b>You are not authorized to use this command.</b>\n\n"
            "Contact Admin for approval.",
            buttons=[Button.url("Contact Admin", "https://t.me/Seiao")],
            parse_mode='html'
        )
        return

    # Check for reply or mentioned user
    reply = await event.get_reply_message()
    text = event.message.text.split()
    target_user = None

    if reply:
        target_user = reply.sender_id
    elif len(text) > 1:
        user_input = text[1]
        if user_input.isdigit():
            target_user = int(user_input)
        elif user_input.startswith('@'):
            try:
                target_entity = await bot.get_entity(user_input)
                target_user = target_entity.id
            except:
                pass

    if not target_user:
        await event.reply(
            "❌ <b>Must reply to a user or mention a valid username/user ID.</b>",
            parse_mode='html'
        )
        return

    chat_id = event.chat_id
    activator = welcome_activators.get((chat_id, target_user))

    # Ensure the sender is the activator or an admin
    if activator and event.sender_id != activator and user_id not in ADMIN_IDS:
        await event.reply(
            "🚫 <b>You cannot stop auto-replies for this user.</b>\n"
            "<i>Only the activator or an admin can use this command.</i>",
            parse_mode='html'
        )
        return

    # Disable auto-replies for the target user
    if chat_id in welcome_targets and target_user in welcome_targets[chat_id]:
        welcome_targets[chat_id].remove(target_user)
        del welcome_activators[(chat_id, target_user)]
        await event.reply(
            f"✅ <b>Auto-replies stopped for user:</b> <code>{target_user}</code>",
            parse_mode='html'
        )
    else:
        await event.reply(
            "⚠️ <b>Auto-replies are not active for this user.</b>",
            parse_mode='html'
        )
        
# Mute command
@bot.on(events.NewMessage(pattern='/chup'))
async def mute_command(event):
    if event.sender_id not in ADMIN_IDS:
        return

    reply = await event.get_reply_message()
    if reply:
        target_user = reply.sender_id
        chat_id = event.chat_id

        if chat_id not in muted_users:
            muted_users[chat_id] = set()

        muted_users[chat_id].add(target_user)
        await event.reply(f"Bot 🔇 Muted for `{target_user}` in This Group.")


# Unmute command
@bot.on(events.NewMessage(pattern='/bol'))
async def unmute_command(event):
    if event.sender_id not in ADMIN_IDS:
        return

    reply = await event.get_reply_message()
    if reply:
        target_user = reply.sender_id
        chat_id = event.chat_id

        if target_user in muted_users.get(chat_id, set()):
            muted_users[chat_id].remove(target_user)
            await event.reply(f"Bot 🔊 Unmuted for `{target_user}` in This Group.")
        else:
            await event.reply("⚠️ User is Not Muted.")

#/id 🆔 CMDs 

@bot.on(events.NewMessage(pattern='/id'))
async def id_command(event):
    # Check if the command is replied to a message
    reply = await event.get_reply_message()

    if reply:
        target_user_id = reply.sender_id
        target_user = await bot.get_entity(target_user_id)
        is_user_approved, time_left = is_approved(target_user_id)

        # Construct the response
        response = (
            f"🦸🏻‍♂️ <b>User Information:</b>\n\n"
            f"👤 <b>Name:</b> {target_user.first_name or 'N/A'}\n"
            f"🆔 <b>User ID:</b> <code>{target_user_id}</code>\n"
            f"🗿 <b>Username:</b> @{target_user.username if target_user.username else 'N/A'}\n"
            f"🎭 <b>Approval Status:</b> {'✅ Approved' if is_user_approved else '🚫 Not Approved'}"
        )

        if is_user_approved:
            response += f"\n<pre>⏳ <b>Time Left:</b> {time_left}</pre>"

        await event.reply(response, parse_mode='html')
    else:
        await event.reply(
            "❌ <b>You must reply to a user to get their details.</b>",
            parse_mode='html'
        )
# Broadcast Command
@bot.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    global broadcasting, waiting_for_broadcast_message, broadcast_message_content

    user_id = event.sender_id

    # Fetch the sender's entity
    sender = await bot.get_entity(user_id)
    sender_username = sender.username

    # Check if the sender is admin by comparing with ADMIN_USERNAME or ADMIN_ID
    if sender_username != ADMIN_USERNAME and user_id != ADMIN_IDS:
        await event.reply("❌ Only Bot Admins Can Use This Command Niggah.")
        return

    # Set flag for broadcasting
    broadcasting = True
    waiting_for_broadcast_message = user_id  # Track that admin is being asked to send a message

    # Notify admin that the bot is ready to receive the message
    await event.reply("📝 Now Send The Message You Want to Broadcast to All Bot Users.")

# Handle Admin Message for Broadcast
@bot.on(events.NewMessage)
async def capture_admin_message(admin_event):
    global broadcasting, waiting_for_broadcast_message, broadcast_message_content

    user_id = admin_event.sender_id

    # Fetch the sender's entity
    sender = await bot.get_entity(user_id)
    sender_username = sender.username

    # Check if the sender is the admin and broadcasting flag is set
    if broadcasting and waiting_for_broadcast_message == user_id and (
        sender_username == ADMIN_USERNAME or user_id == ADMIN_ID
    ):
        broadcast_message = admin_event.text.strip()

        # Validate the broadcast message
        if not broadcast_message or broadcast_message == '/broadcast':
            await admin_event.reply("❌ Broadcast Message Can't Be Empty, Try Again.")
            return

        # Ask the admin for confirmation
        broadcast_message_content = broadcast_message
        broadcasting = False  # Reset the broadcasting flag to avoid conflicts
        waiting_for_broadcast_message = None  # Reset waiting admin ID
        await admin_event.reply(
            f"💬 Do You Want To Broadcast This Message:\n\n{broadcast_message}\n\nConfirm karein:",
            buttons=[
                [Button.inline("Yeahh", b'confirm_yes')],
                [Button.inline("Nopes", b'confirm_no')]
            ]
        )

# Handle Broadcast Confirmation (Yes/No)
@bot.on(events.CallbackQuery)
async def handle_broadcast_confirmation(event):
    global broadcast_message_content

    user_id = event.sender_id

    # Fetch the sender's entity
    sender = await bot.get_entity(user_id)
    sender_username = sender.username

    # Ensure only admin can confirm the broadcast
    if sender_username != ADMIN_USERNAME and user_id != ADMIN_ID:
        await event.answer("❌ Only Bot Admin Can Give Confirmation Bruhh.", alert=True)
        return

    if event.data == b'confirm_yes':
        if not broadcast_message_content:
            await event.answer("❌ Invalid Broadcast Message.", alert=True)
            return

        failed = 0
        sent = 0  # Counter for successfully sent messages

        # Notify admin about the progress
        progress_message = await event.edit(f"📤 Starting Broadcast...\n\n👥 Total users: {len(active_users)}")

        # Send the broadcast message to all users
        for idx, user_id in enumerate(active_users, start=1):
            try:
                await bot.send_message(user_id, broadcast_message_content)
                sent += 1
            except Exception:
                failed += 1

            # Update progress to admin every 10 users
            if idx % 10 == 0 or idx == len(active_users):
                await progress_message.edit(
                    f"📤 Broadcasting...\n\n✅ Sent: {sent}\n❌ Failed: {failed}\n👥 Remaining: {len(active_users) - idx}"
                )

        # Notify admin that broadcast is complete
        await progress_message.edit(
            f"✅ Broadcast Completed!\n\n📤 Sent to: {sent} users\n❌ Failed: {failed}\n👥 Total users: {len(active_users)}"
        )

        # Reset the broadcast message content
        broadcast_message_content = None

    elif event.data == b'confirm_no':
        # If the admin presses 'No', cancel the broadcast
        await event.edit("❌ Broadcast cancelled.")
        broadcast_message_content = None

# Automatically ask for admin when bot joins a new group
@bot.on(events.ChatAction)
async def on_user_join(event):
    if event.user_added and event.user_id == (await bot.get_me()).id:
        chat_id = event.chat_id
        if chat_id not in group_admin_requests:
            group_admin_requests.add(chat_id)
            await bot.send_message(
                chat_id,
                "Yo Lwdo! Must Make Me an Admin of This Group to Fuck Your Target [PythonBotz](t.me/Pythonbotz) !!",
                link_preview=False  # Disable web preview
            )
# Run the bot
bot.run_until_disconnected()
