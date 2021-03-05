import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import datetime

client = discord.Client()

#connect to Spotify API
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(config.CLIENT_ID, config.CLIENT_SECRET))

@client.event
async def on_ready():
    #login msg
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    #if msg read is BOT
    if message.author == client.user:
        return

    if message.content.startswith('$frank'):
        await frankInfo(message)

    elif message.content.startswith('$find'):
        await artistInfo(message)

async def frankInfo(message):
    # Frank Ocean Artist ID
    frankID = 'spotify:artist:2h93pZq0e7k5yf4dywlkpM?si=5Hu58VFzQ4GfnSMzaupIuA'
    artist = sp.artist(frankID)


    album = sp.artist_albums('2h93pZq0e7k5yf4dywlkpM', 'album', 'CA')
    single = sp.artist_albums('2h93pZq0e7k5yf4dywlkpM', 'single', 'CA')

    albumRelease = album['items'][0]['release_date'].split("-")
    dateAlbum = datetime.datetime(int(albumRelease[0]), int(albumRelease[1]), int(albumRelease[2]))

    singleRelease = single['items'][0]['release_date'].split("-")
    dateSingle = datetime.datetime(int(singleRelease[0]), int(singleRelease[1]), int(singleRelease[2]))

    if (dateAlbum > dateSingle):
        mostRecentRelease = album['items'][0]

    else:
        mostRecentRelease = single['items'][0]

    await createEmbededMessage(message, await findMostRecent(frankID))


async def artistInfo(message):
    artistName = str(message.content)[6:]
    artistList = sp.search(q=artistName, limit=10)
    artistID = artistList['tracks']['items'][2]['album']['artists'][0]['id']

    await createEmbededMessage(message, await findMostRecent(artistID))


async def findMostRecent(artistID):

    album = sp.artist_albums(artistID, 'album', 'CA')
    single = sp.artist_albums(artistID, 'single', 'CA')

    albumRelease = album['items'][0]['release_date'].split("-")
    dateAlbum = datetime.datetime(int(albumRelease[0]), int(albumRelease[1]), int(albumRelease[2]))

    singleRelease = single['items'][0]['release_date'].split("-")
    dateSingle = datetime.datetime(int(singleRelease[0]), int(singleRelease[1]), int(singleRelease[2]))

    if (dateAlbum > dateSingle):
        mostRecentRelease = album['items'][0]

    else:
        mostRecentRelease = single['items'][0]

    print(mostRecentRelease)
    return mostRecentRelease

async def createEmbededMessage(message, mostRecentRelease):

    embed = discord.Embed(title=mostRecentRelease['name'],
                          url=mostRecentRelease['external_urls']['spotify'],
                          description="",
                          color=0x109319)
    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="FRANKBOT", url="http://guymorgenshtern.com",
                     icon_url="https://www.pikpng.com/pngl/b/479-4792959_album-cover-art-frank-ocean-blonde-png-download.png")

    embed.set_thumbnail(url=mostRecentRelease['images'][1]['url'])

    embed.add_field(name="Released: ", value=mostRecentRelease['release_date'],
                    inline=False)

    embed.set_footer(text= mostRecentRelease['artists'][0]['name'] + " Most Recent Release")

    await message.channel.send(embed=embed)
    await message.channel.send(mostRecentRelease['external_urls']['spotify'])

client.run(config.token)
