from lyrics_extractor import SongLyrics
import lyrics_extractor

class SongNameNotFound(Exception):
    """LyricMaster Scrping Lyrics Song Not Found Exception."""

class ScrappingError(Exception):
    """LyricMaster Scrapping Error"""

class LyricMasterException(Exception):
    """LyricMaster Exception Errors"""

class SongError(Exception):
    """Other LyricMaster API Song Exceptions."""

class Lyrics():
    def __init__(self, APIKey : str = None, EngineID : str = None):
        """
        ---!INSERT INFO HERE!---
        """
        if APIKey == None:
            ApiKey = "AIzaSyCd2mUKNe8eGbTvDfTgE8fdKEMvdt3vyYU"
        
        if EngineID == None:
            EngineID = "3d527b3474c25fe39"

        self.API = ApiKey
        self.Engine = EngineID

    def get_lyric(self, *, SongName = None):
        """
        Gets the Lyrics of a Song Name

        Usage: get_lyric(Song_Name)
        ~~~~~~~~~~~~~~~~
        
        Example: print(get_lyric(Despacito))

        Returns: A Dict e.g.
        {
            'title': str(The Title Of The Song)
            'lyric': str(The Lyrics Of The Song)
        }

        To get the title, You can do: get_lyric(SongName)['title']

        To get the lyric, You can do: get_lyric(SongName)['lyric']
        """

        if SongName == None:
            raise SongError({'Error': 'SongName not defined! Usage: \"get_lyric(SongName)\"!'})

        try:
            lyrics = SongLyrics(self.API, self.Engine)

            getlyrics = lyrics.get_lyrics(str(SongName))

            totaljson = {
                "title": str(SongName).lower().title() if str(getlyrics) == "" or str(getlyrics) == None else str(getlyrics['title']).title(),
                "lyric": str(getlyrics['lyrics'])
            }
            return totaljson
        except lyrics_extractor.LyricScraperException:
            raise SongNameNotFound({'Error': "Song Named {} Not Found!".format(SongName)})