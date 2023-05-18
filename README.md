# CSSE432-Final-Project

## Spandora Project Description
Spandora is an app that allows you to queue music to play with your friends. This is code for a web server that runs on a host machine. Users can connect to the host machine through their browser. The client program works via phone or computer, as long as it runs a modern browser. These clients will be able to view the current queue of songs, see which songs the server can play, and add songs to the queue. Additionally, clients can upload their own music files to the server to add to the queue (if the song is properly formatted). Spandora can be used socially in small group settings or commercially by restaurants and other venues.

## How to Run
Starting the backend: ```python3 ./testREST.py```

Starting the web client: ```python3 ./webserver.py```

**Note:** The backend SQL database is going to be taken offline so I can pack for the summer. If you want to run the complete project, you will need to create your own database according to the schema below.

## API Endpoints

| **API Endpoint** | **Type** | **Returns** | **Description**                                                          |
|------------------|----------|-------------|--------------------------------------------------------------------------|
| /api/songlist    | GET      | JSON        | Returns all song names, song ids, and artist names in database           |
| /api/queue       | GET      | JSON        | Returns all song names, artist names, and album names in queue           |
| /api/play        | GET      | String      | Starts playing (or resumes) first song in queue                          |
| /api/pause       | GET      | String      | Pauses the currently playing song                                        |
| /api/resume      | GET      | String      | Resumes the paused song                                                  |
| /api/stop        | GET      | String      | Stops the currently playing (or paused) song and drops it from the queue |
| /api/create      | POST     | None        | Adds new song file to database and storage directory                     |
| /api/insert      | POST     | None        | Inserts passed song id into queue                                        |

## Functions
| **Function**          | **Arguments** | **Returns** | **Description**                                                          |
|-----------------------|---------------|-------------|--------------------------------------------------------------------------|
| getSongList()         | None          | JSON Array  | Returns all songs in database with format: Song_Name,Song_ID,Artist_Name |
| addSongtoDB()         | songData      | None        | Parses metadata and adds song to database                                |
| removeSongfromQueue() | songID        | None        | Removes given ID from queue                                              |
| getSongQueue()        | None          | JSON Array  | Returns all songs in queue with format: Song_Name,Artist_Name,Album_Name |
| playSong()            | None          | None        | Begins playing song at top of queue, then removes from queue             |
| pauseSong()           | None          | None        | Pauses the currently playing song                                        |
| stopSong()            | None          | None        | Stops the currently playing or paused song                               |

## Database Schema
| **Column** | **Type** | **Description** |
|------------|----------|-----------------|
| Song_Name  | String   | Name of song    |
| Artist_Name| String   | Name of artist  |
| Album_Name | String   | Name of album   |
| Genre      | String   | Genre of song   |
| Song_Length| Double   | Song length (s) |
| Song_Path  | String   | Path to file    |
| Song_ID    | Integer  | Unique ID       |

