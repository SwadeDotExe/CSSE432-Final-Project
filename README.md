# CSSE432-Final-Project

## Spandora Project Description
Spandora is an app that allows you to queue music to play with your friends. This is code for a web server that runs on a host machine. Users can connect to the host machine through their browser. The client program works via phone or computer, as long as it runs a modern browser. These clients will be able to view the current queue of songs, see which songs the server can play, and add songs to the queue. Additionally, clients can upload their own music files to the server to add to the queue (if the song is properly formatted). Spandora can be used socially in small group settings or commercially by restaurants and other venues.

## How to Run
First navigate to the ```/WebServer``` directory.

Starting the backend (API): ```python3 ./testREST.py```

Starting the web server: ```python3 ./webserver.py```

At this point, you should be able to go to the web client in your browser through localhost (or the IP of the machine) on port 8080. The backend API runs on port 9000. (You can change both of these port numbers by modifying various places in the code). *However,* you will not be able to use the API without changing the API at the top of the file ```scripts/main.js```. You will want to change line 14 to be ```const apiUrl = "http://changeme:9000/api/";``` where changeme is your local machine IP or localhost.

**Note:** The backend MySQL database is going to be taken offline so I can pack for the summer. If you want to run the complete project, you will need to create your own MySQL database according to the schema below. You will also likely need to change the API code to reflect the new domain and login of the database. If you plan on using a real password or secure database, you should probably look into using encryption instead of putting it in plaintext like it is here.

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

### Song Library
The Song Library keeps track of all songs that the server has as well as their respective file locations. It also tracks all other metadata for songs like the artist name and album name, and a unique integer ID for each song. This ID is used for retrieving specific information and identification by the frontend JavaScript and also for use in the Queue (essentially it is a primary key for Song Library and foreign key for Queue).
| **Column** | **Type** | **Description** |
|------------|----------|-----------------|
| Song_Name  | String   | Name of song    |
| Artist_Name| String   | Name of artist  |
| Album_Name | String   | Name of album   |
| Genre      | String   | Genre of song   |
| Song_Length| Double   | Song length (s) |
| Song_Path  | String   | Path to file    |
| Song_ID    | Integer  | Unique ID       |

### Queue
The Queue just keeps track of all current songs in the queue by ID (a foreign key for the ID in Song Library), and when songs finish playing or are skipped then they are removed from the queue. Likewise, adding a song from the web client will make a database call to add a song to the queue. If you write your own implementation of the database schema, this could instead be implemented as a server-side data structure. The downside of that approach is your queue will not persist between server crashes or restarts.
| **Column** | **Type** | **Description** |
|------------|----------|-----------------|
| Song_ID    | Integer  | Unique ID       |
