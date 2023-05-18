# CSSE432-Final-Project

API Endpoints:

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