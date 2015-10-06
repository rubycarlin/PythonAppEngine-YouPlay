#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
sys.path.insert(0, 'libs')

import os
import webapp2
import jinja2
import os
import urllib
import logging
import urllib3
import urllib2
import json
import random

from bs4 import BeautifulSoup

from apiclient.discovery import build
from optparse import OptionParser

DEVELOPER_KEY = "AIzaSyAeAk0HA78hE0SLaK6FgPhLTPVf08grK7s"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class SearchHandler(webapp2.RequestHandler):
	def get(self):
		template_values = []
		self.response.headers['Content-type'] = 'text/html' 
		template = JINJA_ENVIRONMENT.get_template('searchresult.html')
		self.response.write(template.render(template_values))

	def post(self):
		q = self.request.get('searchBar');
		video_data = self.search(q);
		song =[]
		video_id = []
		lyric_url = []
		for data in video_data:
			#logging.debug("line is %s", data)
			split_arr = data.split("@$#")
			#rand_no = random.randint(1, len(split_arr))
			#split_arr = split_arr[rand_no:] + split_arr[:rand_no]
			if len(split_arr) == 3:
				song += [split_arr[0]]
				video_id += [split_arr[1]]
				lyric_url += [split_arr[2]]

		template_values = {'songs' : song, 'videoids' : video_id, 'lyric_urls' : lyric_url}
		self.response.headers['Content-type'] = 'text/html'
		template = JINJA_ENVIRONMENT.get_template('searchresult.html')
		self.response.write(template.render(template_values))
	#	self.response.write(html);
		
	def search(self, query):
		artists = ['5 Seconds Of Summer', 'ASAP Rocky', 'Adam Levine', 'Alabama', 
		'Alessia Cara', 'Andy Grammer', 'Andy Mineo', 'Ariana Grande', 
		'Atreyu', 'Beyonce', 'Big Sean', 'Blake Shelton', 'Brett Eldredge', 
		'Bruno Mars', 'Cam', 'Carrie Underwood', 'Charlie Puth', 'Chris Brown', 
		'Chris Cornell', 'Chris Janson', 'Cole Swindell', 'DJ Snake', 'David Gilmour', 
		'Demi Lovato', 'Dr Dre', 'Drake', 'Ed Sheeran', 'Elle King', 'Ellie Goulding', 
		'Eminem', 'Eric Church', 'Fall Out Boy', 'Fetty Wap', 'Fifth Harmony', 
		'Five Finger Death Punch', 'Florida Georgia Line', 'Future', 'Hailee Steinfeld', 
		'Halsey', 'Hozier', 'Imagine Dragons', 'J Cole', 'Jason Aldean', 'Jason Derulo', 
		'Jeremih', 'John Legend', 'Justin Bieber', 'K Camp', 'Kanye West', 'Katy Perry', 
		'Keith Richards', 'Keith Urban', 'Kendrick Lamar', 'Kenny Chesney', 'Lady Gaga', 
		'Lana Del Rey', 'Little Mix', 'Luke Bryan', 'Mac Miller', 'Macklemore & Ryan Lewis', 
		'Maddie & Tae', 'Major Lazer', 'Mark Ronson', 'Maroon 5', 'Meek Mill', 'Meghan Trainor', 
		'N W A', 'Nick Jonas', 'Nicki Minaj', 'OMI', 'Old Dominion', 'One Direction', 'R City', 
		'Rachel Platten', 'Rae Sremmurd', 'Remy Boyz', 'Rich Homie Quan', 'Rihanna', 'Ryan Adams', 
		'Sam Hunt', 'Sam Smith', 'Selena Gomez', 'Shawn Mendes', 'Shinedown', 'Sia', 'Silento', 
		'Taylor Swift', 'The Weeknd', 'Thomas Rhett', 'Tove Lo', 'Travis Scott', 'Trey Songz', 
		'Turnpike Troubadours', 'WALK THE MOON', 'Wiz Khalifa', 'X Ambassadors', 'Zac Brown Band', 
		'blessthefall', 'iHeartMemphis', 'twenty one pilots']

		artist_index = artists.index(query)
		file_no = (artist_index / 10) + 1
		line_no = ( artist_index % 10 ) + 1
		song_list = self.openfile(file_no, line_no)
		return(song_list);
		"""
		youtube = build(
			YOUTUBE_API_SERVICE_NAME, 
			YOUTUBE_API_VERSION, 
			developerKey=DEVELOPER_KEY)
		search_response = youtube.search().list(
			q=query,
			part="id,snippet",
			order="relevance",
			type="video",
			maxResults=1
			).execute()

		videos = []
		channels = []
		playlists = []

		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				videos.append("%s" % search_result["id"]["videoId"])

		params = {
			"method" : "artist.getTopAlbums",
			"artist" : query,
			"limit" : 5,

		}
		return(videos)
		"""

	def openfile(self, file_no, line_no):
		logging.debug("File no is %d and line no is %d", file_no, line_no)
		path = os.path.join(os.path.split(__file__)[0], "songs\\" + str(file_no) + '.txt')
		logging.debug("Path is %s", path)
		curr_line = 0;
		song_list = []
		f = open(path, 'r')
		curr_line = 1;
		for line in f:
			if curr_line == line_no:
				return(line.split("@$#*"))
			curr_line += 1

		return(song_list)

class LyricHandler(webapp2.RequestHandler):
	def post(self):
		lyric_url = self.request.get('lyricurl');
		lyrics = ""
		lyric_resp = ""
		logging.debug("Lyric url is %s", lyric_url)
		if(lyric_url != None):
			try:
				usock = urllib2.urlopen(lyric_url)
				lyric_resp = usock.read()
				#logging.debug("LyricBoxTag is %s", lyric_resp)

				usock.close()
				soup = BeautifulSoup(lyric_resp)
				lyricBoxTags = soup.find_all("div", class_='lyricbox')
				logging.debug("Length of lyricBoxTags : %d", len(lyricBoxTags))
				for lyricBoxTag in lyricBoxTags:
					s = str(lyricBoxTag)
					#logging.debug("LyricBoxTag is %s", s)

					#print s
					inner_soup = BeautifulSoup(s)

					#[s.extract() for s in inner_soup('script')]
					inner_soup.script.decompose()
					inner_soup.script.decompose()

					lyrics = str(inner_soup)
					logging.debug("Lyrics is %s", lyrics)
					#print lyrics
					if(lyrics != ""):
						break;
				return webapp2.Response(lyrics)
			except:
				pass
			#http = urllib3.PoolManager()
			#lyric_resp = http.request('GET', lyric_url)
			#lyric_resp = requests.get(lyric_url)

		else:
			return webapp2.Response("NOT OK")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/getlyric', LyricHandler)
], debug=True)
