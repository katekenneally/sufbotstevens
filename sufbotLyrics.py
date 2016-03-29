# Kate Kenneally
# sufbotLyrics.py
# Based on @tmbotg code by @bgporter

from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import random

baseUrl = "http://www.lyricsmode.com"

def getSoup(urlFragment):
    data = requests.get(urljoin(baseUrl, urlFragment))
    soup = BeautifulSoup(data.text, "html.parser")
    return soup
   
def processSong(url):
    '''Returns list of lyrics for provided song; url = link to song page'''
    soup = getSoup(url)
    data = soup.find("p",attrs={"class": "ui-annotatable"}) # find lyrics
    strippedLyrics = str(data).strip('<p class="ui-annotatable" id="lyrics_text">').strip("</").split("\n") # strip unwanted characters
    completeLyrics = []
    for l in strippedLyrics:
        new = l.replace("<br/>","") # use replace instead of strip to avoid cutting off r's and b's in actual lyrics
        if len(new)!=0: # get rid of empty lines
            completeLyrics.append(new)
    return completeLyrics
      
def processArtist(url):
    '''Returns list of songs for provided artist; url = link to artist page'''
    soup = getSoup(url)
    data = soup.findAll("a",attrs={"class": "ui-song-title"}) # get data for each song
    urls = []
    for s in data:
        lastIndex1 = str(s).rfind('href=') # start at unique point
        lastIndex2 = str(s).rfind('html') # end at unique point
        new = str(s)[lastIndex1:lastIndex2+5].strip('href="') # slice string and strip unwanted characters
        urls.append(new)
    return urls

def getRandomLyrics(songList):
    '''Returns a list of random lyrics given a list of songs'''
    songIndex = random.randint(0,len(songList)-1) # randomly choose a song
    url = baseUrl + songList[songIndex] # generate url
    lyrics = processSong(url) # get list of lyrics
    numLines = random.randint(1,5) # randomly choose number of lines to tweet
    lyricIndex = random.randint(0,len(lyrics)-numLines) # randomly choose a starting lyric
    # subtracting numLines eliminates the possibility of a list index out of range IndexError
    tweetedLyrics = []
    for i in range(numLines): # append the chosen number of consecutive lines
        if "[Incomprehensible]" in lyrics[lyricIndex+i]: # LyricsMode isn't the most accurate at transcribing lyrics
            print 'ERROR: Lyrics contained "[Incomprehensible]", trying again'
            getRandomLyrics(songList)
        else:
            tweetedLyrics.append(lyrics[lyricIndex+i])
    return tweetedLyrics
    
sufjanList = processArtist("http://www.lyricsmode.com/lyrics/s/sufjan_stevens/")