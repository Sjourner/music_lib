General idea:
-------------


IMPORTANT:
sqlite has a good test database, which is exactly what I need,
you can download it and add a few fields here and there (like "track type","should be seen live", etc.),
and drop a few unnecessary tables and relationships (employees)
https://www.sqlitetutorial.net/sqlite-sample-database/ 

The chinook.db it is. However, you cannot really drop columns (boo!).
But there is a workaround here
https://stackoverflow.com/questions/8442147/how-to-delete-or-add-column-in-sqlite

You have already created music.db 

Create a web application, where:
- User has a view (main menu) to select between the following views:
  - overview
  - suggest-a-band
  - add new band
  - add favourite track
  - favourites
- user has a view to add a band which the user has just discovered
- the application looks up automaticly the associated genres
  from rateyourmusic
- the application looks up automaticly a list of albums
  from rateyourmusic
    - this should happen per default once per adding a band
    - with a possibility to manually re-load the list of albums
- user has a view to select a band from the previously added ones
  and add information:
    - favourite track(s) (multiples should be allowed)
      - possibly mark an album for all favourite
      - automatically save the timestamp, when a favourite track/album
        was added
    - short review about the band
    - mark, if a band should be listened live or not
    - mark, if the whole discography was listened.
      - this should be not connected to rateyourmusic
- User has a view wich list all genres and a percentage share, how
  many bands are marked as "listened" from all added bands
- User should have a "suggest-a-band" page
  - User should be able a genre and the first, non-"listened" band
    should be returned.
    - Optional: maybe show the last favourite track to
      help users, which track was listened recently
- User should have a view to look up a band and see all the favourite
    tracks from them
    - nice-to-have: it would be cool to generate a youtube link for them

SQL structure

CREATE TABLE IF NOT EXISTS "artists"
(
    [ArtistId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [Name] NVARCHAR(120) NULL,
    [Comment] NVARCHAR(120) NULL,
    [See_live] INTEGER DEFAULT 0 
);
CREATE TABLE IF NOT EXISTS "genres"
(
    [GenreId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [Name] NVARCHAR(120)
);
CREATE TABLE IF NOT EXISTS "albums"
(
    [AlbumId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [Title] NVARCHAR(160)  NOT NULL,
    [ArtistId] INTEGER  NOT NULL,
    [Listened] DEFAULT 0,
    [Last_modified] DATETIME NOT NULL,
    FOREIGN KEY ([ArtistId]) REFERENCES "artists" ([ArtistId]) 
);
CREATE TABLE IF NOT EXISTS "tracks"
(
    [TrackId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [Name] NVARCHAR(200)  NOT NULL,
    [ArtistId] INTEGER,
    [AlbumId] INTEGER,
    [Track_type] INTEGER,
    [Entry_date] DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ([ArtistId]) REFERENCES "artists" ([ArtistId])
);
CREATE INDEX [IFK_AlbumArtistId] ON "albums" ([ArtistId]);
CREATE INDEX [IFK_TrackAlbumId] ON "tracks" ([AlbumId]);
CREATE INDEX [IFK_TrackArtistId] ON "tracks" ([ArtistId]);
