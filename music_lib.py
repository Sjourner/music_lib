#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Máté Szegedi"
__version__ = "0.1.0"
__license__ = "GNU"

import sqlite3
import pandas as pd
import sys
import getopt
import argparse

class Music:
    def __init__(self):
        #create connection
        self.connection = sqlite3.connect('music.db')
        self.cursor = self.connection.cursor()

    def test_query(self):
        #test query
        test_query = "SELECT * FROM [genres];"
        print(test_query)
        test_run = pd.read_sql_query(test_query, self.connection)
        print(test_run)

    def last_tracks(self,tracks=10):
        #lists you the last X tracks (default = 10)
        query = """SELECT 
                    art.[Name] AS 'Artist'
                    ,tra.[Name] AS 'Track'
                    ,tra.[Track_type] AS [Track_type]
                    ,tra.[Entry_date] AS 'Last_entry' 
                    FROM [tracks] AS tra 
                    LEFT JOIN [artists] AS art 
                    ON tra.[ArtistId] = art.[ArtistId] 
                    ORDER BY tra.[Entry_date] DESC 
                    LIMIT """ + str(tracks) + ";"
        last_10_tracks = pd.read_sql_query(query, self.connection)
        print(last_10_tracks)

    def add_track(self,band,song,track_type):
        #adds a new track to the list you have listened

        #first check, if you have already this artist on your list
        art_query = """SELECT [ArtistId]
                    FROM [artists]
                    WHERE [Name] =  """ + "'" +str(band) + "';"
        check_artist = pd.read_sql_query(art_query, self.connection)
        # if artist exists in database
        if len(check_artist) == 0:
            # if this is new, add to the database
            art_insert_query = """ INSERT INTO [artists] ([Name])
                                    VALUES (""" + "'" + str(band) +"');" 
            self.connection.execute(art_insert_query)
            self.connection.commit()   
        # Get the Artist ID of the artist into a variable
        artist_id = pd.read_sql_query(art_query, self.connection)
        artist_id = artist_id["ArtistId"][0]

        # Check if the song exists from this author in the database
        song_query = """SELECT 
                    tra.[ArtistId] AS 'Artist'
                    ,tra.[Name] AS 'Track'
                    FROM [tracks] AS tra
                    WHERE [ArtistId] = """ + "'" + str(artist_id) + """'
                    AND [Name] = """ + "'" + str(song) + """'
                    AND [Track_type] = """+ "'" + str(track_type) + "';" 
        
        # print(song_query)
        song_match = pd.read_sql_query(song_query, self.connection)
        if len(song_match) == 0:
            #if this is a new song, add to the database
            song_insert_query = """ INSERT INTO [tracks]
                                ([ArtistID],[Name],[Track_type])
                                VALUES (""" + "'" + str(artist_id) + "','"+ str(song)+ "','"+ str(track_type) + "');"
            self.connection.execute(song_insert_query)
            self.connection.commit()
            print("insert is done")
        else:
            return print("This song is already in the database")

def main(argv):
    #initialize connection object
    current_music = Music()
    # run the right command based on the argument
    if argv[0] == "add_track":
        return current_music.add_track(argv[1],argv[2],argv[3])
    elif argv[0] == "test_query":
        return current_music.test_query()
    elif argv[0] == "last_tracks":
        if len(argv) > 1:
            return current_music.last_tracks(argv[1])
        else:
            return current_music.last_tracks(10)
    else:
        return print("wrong command was used")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    if len(sys.argv) < 2:
        print ("Enter at least one command after music_lib.py")
    else:
        main(sys.argv[1:])



