# Kate Kenneally
# sufbot.py
# Based on @tmbotg code by @bgporter

from datetime import datetime
from datetime import date
from glob import glob
from pprint import pprint
from random import choice
from random import random
from time import time
from twython import Twython
from twython import TwythonStreamer
from twython.exceptions import TwythonError

import os.path

import sufbotLyrics

defaultConfigDict = {
   "appKey"             : "",
   "appSecret"          : "",
   "accessToken"        : "",
   "accessTokenSecret"  : "",
}

# key/token information removed

class Sufbot(object):
    def __init__(self, argDict=None):
        if not argDict:
            argDict = {"force": False, 'stream': False}
            # update this object's internal dict with the dict of args that was passed
            # in so we can access those values as attributes.   
        self.__dict__.update(argDict)
        self.tweet = ""
        self.settings = defaultConfigDict
        s = self.settings
        self.twitter = Twython(s['appKey'], s['appSecret'], s['accessToken'], s['accessTokenSecret'])
         
         
    def SendTweets(self):
        ''' send each of the status updates that are collected in self.tweets 
        '''
        self.twitter.update_status(status=self.tweet)
            
    def Run(self):
        self.GetLyric()
        self.SendTweets()
         
    def GetLyric(self):
        sufjanList = sufbotLyrics.processArtist("http://www.lyricsmode.com/lyrics/s/sufjan_stevens/")
        charcount = 141
        while charcount>140: # ensure tweet is 140 characters or less (twitter character limit)
            lyrics = sufbotLyrics.getRandomLyrics(sufjanList)
            charcount = 0
            for l in lyrics:
                charcount+=len(l)
        tweet = ""
        for l in lyrics:
            tweet+=l+"\n"
        self.tweet = tweet

         
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true', 
        help="print to stdout instead of tweeting")
    parser.add_argument("--force", action='store_true', 
        help="force operation now instead of waiting for randomness")
    parser.add_argument("--stream", action="store_true", 
        help="run in streaming mode")
    args = parser.parse_args()
    argDict = vars(args)
    bot = Sufbot(argDict)
    bot.Run()