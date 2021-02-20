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
    if (message.content.startswith('$embed')):
        embed()
    if message.content.startswith('$hello'):
        #Frank Ocean Artist ID

        frankID = 'spotify:artist:2h93pZq0e7k5yf4dywlkpM?si=5Hu58VFzQ4GfnSMzaupIuA'
        artist = sp.artist(frankID)


        album = sp.artist_albums('2h93pZq0e7k5yf4dywlkpM', 'album')
        single = sp.artist_albums('2h93pZq0e7k5yf4dywlkpM', 'single')

        albumRelease = album['items'][0]['release_date'].split("-")
        dateAlbum = datetime.datetime(int(albumRelease[0]), int(albumRelease[1]), int(albumRelease[2]))

        singleRelease = single['items'][0]['release_date'].split("-")
        dateSingle = datetime.datetime(int(singleRelease[0]), int(singleRelease[1]), int(singleRelease[2]))

        if (dateAlbum > dateSingle):
            await message.channel.send("Frank Ocean's Most Recent Release: " + album['items'][0]['name'] + " "
                                   + album['items'][0]['release_date'])
        else:

            await message.channel.send("Frank Ocean's Most Recent Release: " + single['items'][0]['name'] + " "
                                       + single['items'][0]['release_date'])

            await message.channel.send(single['items'][0]['external_urls']['spotify'])

        '''
        for album in album['items']:

            releaseDate = album['release_date'].split("-")
            print(releaseDate)
            d1 = datetime.datetime(int(releaseDate[0]), int(releaseDate[1]), int(releaseDate[2]))

            if (d1 > mostRecent):
                mostRecent = d1
                await message.channel.send("Frank Ocean's Most Recent Release: " + album['name'] + " " 
                                           + album['release_date'])
        '''



client.run(config.token)
