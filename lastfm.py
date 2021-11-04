# Some parts are Copyright (C) LakesideMiners (@LakesideMiners) 2021-Present
# I DO NOT OFFER ANY SUPPORT!
# All licensed under project license
#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import requests
import json
from .. import loader, utils
logger = logging.getLogger(__name__)

# Setup all the config bs
@loader.tds
class LastfmMod(loader.Module):
    """Get LastFM Last Played
       Get an API key and Secret at https://www.last.fm/api/account/create"""
    strings = {"name": "LastFM",
               "doc_username": "Your LastFM Username",
               "doc_api_key": "API Key from https://www.last.fm/api/account/create"
               }

    def __init__(self):
        self.config = loader.ModuleConfig("USERNAME", None, lambda m: self.strings("doc_username", m),
                                          "API_KEY", None, lambda m: self.strings("doc_api_key", m)
                                          )


    # When we type ".np" we get the curretnly playing song of the LastFM user in the config. Else, get the last played song 
    async def npcmd(self, message):
        """Print The Currently Playing Song On LastFM, last played if no song is playing.""" 
        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + str(self.config["USERNAME"]) + '&' + 'api_key=' + str(self.config["API_KEY"]) + '&format=json' + '&limit=1')
        json_output = r.json()
        try:
            playing = json_output['recenttracks']['track'][0]['@attr']['nowplaying']
            pass
        except KeyError:
            playing = False
            pass

        if playing == 'true':
            track_name = json_output['recenttracks']['track'][0]['name']
            artist_name = json_output['recenttracks']['track'][0]['artist']['#text']
            album_name = json_output['recenttracks']['track'][0]['album']['#text']
            song_url = json_output['recenttracks']['track'][0]['url'] 
            formated_message = "Now Playing" + "\n" + "Track: " + track_name + "\n" + "Artist: " + artist_name + "\n" + "Album: " + album_name + "\n" + "Song URL: " + song_url
            await utils.answer(message, str(formated_message))
        else:
            track_name = json_output['recenttracks']['track'][0]['name']
            artist_name = json_output['recenttracks']['track'][0]['artist']['#text']
            album_name = json_output['recenttracks']['track'][0]['album']['#text']
            song_url = json_output['recenttracks']['track'][0]['url']
            date_played = json_output['recenttracks']['track'][0]['date']['#text']
            formated_message = "Last Played" + "\n" + "Track: " + str(track_name) + "\n" + "Artist: " + str(artist_name) + "\n" + "Album: " + str(album_name) + "\n" + "Song URL: " + str(song_url) + "\n" + "Date Played: " + str(date_played) + " UTC"
            await utils.answer(message, str(formated_message))
