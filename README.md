# CSSE432-Final-Project

## API Endpoints:

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
| Song_ID    | String   | Unique ID       |
| Artist_Name| String   | Name of artist  |
| Album_Name | String   | Name of album   |
| File_Name  | String   | Name of file    |
| File_Path  | String   | Path to file    |

