import discord, asyncio, easyocr, io, aiohttp, numpy as np
from discord.errors import DiscordServerError, HTTPException
from patterns import PATTERNS
from exclusions import EXCLUDED_CHANNEL_IDS
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

TOKEN = "INSERT_BOT_TOKEN"
REPLY_MESSAGE = "No."

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name='The Demise of Why-Am-So 🔥'))
    
    for guild in client.guilds:
        print(f"Checking guild: {guild.name}")
        channels = guild.text_channels
        excluded_count = 0
        for channel in channels:
            if channel.id in EXCLUDED_CHANNEL_IDS:
                channels.remove(channel)
                excluded_count += 1
        print(f"Processed {len(channels)}/{len(channels) + excluded_count} text channels in {guild.name}.")
    
    while True:
        await check_messages(channels)

async def check_messages(channels):
    for channel in channels:
        await check_channel_messages_with_retries(channel)

async def check_channel_messages_with_retries(channel, retries=3, delay=5):
    for attempt in range(retries):
        try:
            await check_channel_messages(channel)
            return
        except (DiscordServerError, HTTPException) as e:
            print(f"Error checking {channel.name}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds ...")
                await asyncio.sleep(delay)
            else:
                print(f"Max retries reached for {channel.name}. Skipping.")

async def check_channel_messages(channel):
    messages = []
    async for message in channel.history(limit=5):
        messages.append(message)
    messages.reverse()

    if client.user == messages[-1].author or messages[-1].author.id == 863825474215608321:
        # print(f"Skipping channel {channel.name} because the bot or owner sent the earliest message.")
        return

    concatenated_content = "".join(msg.content for msg in messages).upper().replace(" ", "")
    
    # Extract text from image attachments
    async with aiohttp.ClientSession() as session:
        for message in messages:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith(("png", "jpg", "jpeg", "gif", "bmp", "webp", "svg", "ico", "cur")):
                    image_url = attachment.url
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            image_bytes = await response.read()
                            image = Image.open(io.BytesIO(image_bytes))
                            image_np = np.array(image)  # Convert PIL Image to numpy array
                            text = reader.readtext(image_np, detail=0)
                            concatenated_content += "".join(text).upper().replace(" ", "")
                            print(f"Concatenated {text} to the content. (OCR)")
                        else:
                            print("Error fetching image:", response.status)

    # Check each regex pattern
    for pattern in PATTERNS:
        if pattern.search(concatenated_content):
            print(f'Concatenated content in {channel.name}: "{concatenated_content}"\nFound a match with pattern #{PATTERNS.index(pattern) + 1} in {channel.name}.')
            await send_reply(channel, messages[-1])
            await react_to_message(messages[-1])
            break

async def send_reply(channel, message):
    try:
        await channel.send(REPLY_MESSAGE, reference=message)
    except discord.Forbidden:
        print(f"Permission error: Cannot send messages in {channel.name}.")
    except Exception as e:
        print(f"Unexpected error while sending a reply: {e}")

async def react_to_message(message):
    try:
        await message.add_reaction("❌")
    except discord.Forbidden:
        print("Permission error: Cannot add reactions.")
    except Exception as e:
        print(f"Unexpected error while reacting to message: {e}")

client.run(TOKEN)