/**
 * @fileoverview
 * Provides the JavaScript interactions for main Spandora page.
 *
 * @author 
 * William Foss
 */

/* namespace */
var spandora = spandora || {};

/* globals */
spandora.variableName = "";
const apiUrl = "http://137.112.201.216:9000/api/";
spandora.pageController = null;
spandora.songServerManager = null;
spandora.startedPlaying = false;

// From: stack overflow
function htmlToElement(html) {
	var template = document.createElement(`template`);
	html = html.trim();
	template.innerHTML = html;
	return template.content.firstChild;
}

spandora.PageController = class {
    /* Creates page constructor and all interactive events for buttons */
    constructor() {
        this._searchedSongID = null;

        document.querySelector("#playBtn").onclick = (event) => {
            if (spandora.startedPlaying == false) {
                spandora.songServerManager.playSong();
                spandora.startedPlaying = true;
            }
            else {
                spandora.songServerManager.resumeSong();
            }
		}

        document.querySelector("#pauseBtn").onclick = (event) => {
			spandora.songServerManager.pauseSong();
		}

        document.querySelector("#skipBtn").onclick = (event) => {
			spandora.songServerManager.skipSong();
		}

        document.querySelector("#submitUpload").onclick = (event) => {
            spandora.songServerManager.uploadSong();
        } 

        this.initializeView();

        setInterval(this.initializeView(), 20000);
    }

    initializeView() {
        this.updateQueue();
        this.updateSongList();
    }

    updateQueue() {
        // Passes queue request to server which returns queue of songs
        spandora.songServerManager.getQueue()
        .then((data) => {
            this._updateQueueHelper(data)
        })
        .catch(err => {
			console.log(err);
		});
	}

    _updateQueueHelper(data) {
        let fullQueueList = data;
        const newQueue = htmlToElement(`<div id="queueListContainer" class="songQueueDiv"></div>`);
		for (let i = 0; i < fullQueueList.length; i++) {
            // Get item from json
            const song = new spandora.SongFromQueue(fullQueueList[i]);
			const newSong = this._createQueuedSong(song);
			newQueue.appendChild(newSong);
		}
		const oldQueue = document.querySelector("#queueListContainer");
		oldQueue.removeAttribute("id");
		oldQueue.hidden = true;
		oldQueue.parentElement.appendChild(newQueue);
    }

    _createQueuedSong(song) {
		return htmlToElement(`
        <div class="card">
            <div class="card-body">
                <h5 class="card-title d-flex justify-content-between align-items-center">
                    <div>
                        ${song.songName}
                    </div>
                </h5>

                <h6 class="card-subtitle mb-2 text-muted">
                    <div>
                        ${song.artist}
                    </div>
                </h6>
            </div>
        </div>`);
	}

    updateSongList() {
        // Passes song request to server which returns song list
        spandora.songServerManager.getSongs()
        .then((data) => {
            console.log(data);
            this._updateSongListHelper(data)
        })
        .catch(err => {
			console.log(err);
		});
	}

    _updateSongListHelper(data) {
        let fullSongList = data;
        const newSongList = htmlToElement(`<div id="songListContainer" class="songListDiv"></div>`);
        for (let i = 0; i < fullSongList.length; i++) {
            // Get item from json as a song
            let stringData = fullSongList[i].split("_");
            const song = new spandora.SongFromList(stringData);
            // Create songs and add them to the page
            const newSong = spandora.pageController._createListedSong(song);
            let songButton = newSong.querySelector("#num" + song.id);
            songButton.onclick = (event) => {
				this._searchedSongID = songButton.id;
                spandora.songServerManager.addToQueue(this._searchedSongID)
                .then((response) => {
                    this.updateQueue();
                })
                .catch(err => {
                    console.log(err);
                });
			}
            newSongList.appendChild(newSong);
        }
        const oldSongList = document.querySelector("#songListContainer");
        oldSongList.removeAttribute("id");
        oldSongList.hidden = true;
        oldSongList.parentElement.appendChild(newSongList);
    }

    _createListedSong(song) {
		return htmlToElement(`
        <div class="card songsList">
            <div class="card-body">
                <h5 class="card-title d-flex justify-content-between align-items-center">
                    <div class="songName">
                        ${song.songName}
                    </div>
                </h5>

                <h6 class="card-subtitle mb-2 text-muted artist">
                    <div class="artist">
                        ${song.artist}
                    </div>
                </h6>

                <div class="text-center">
                    <button id="num${song.id}" type="button" class="btn bmd-btn-fab queueFab">
                        <i class="material-icons">add</i>
                    </button>
                </div>
            </div>
        </div>`);
	}

    searchSongs() {
        let input = document.getElementById('songSearchBar').value
        input=input.toLowerCase();
        let songsList = document.getElementsByClassName('songsList');
          
        for (let i = 0; i < songsList.length; i++) { 
            if (!songsList[i].querySelector(".songName").innerHTML.toLowerCase().includes(input) &&
                !songsList[i].querySelector(".artist").innerHTML.toLowerCase().includes(input)) {
                songsList[i].style.display="none";
            }
            else {
                songsList[i].style.display="inherit";                 
            }
        }
    }

}

/** Song Class for making things easier */
spandora.SongFromList = class {
	constructor(songData) {
        // console.log(songData);
		this.songName = songData[0];
        this.id = songData[1];
		this.artist = songData[2];
	}
}

spandora.SongFromQueue = class {
	constructor(songData) {
        // console.log(songData);
		this.songName = songData[0];
        this.artist = songData[1];
		this.album = songData[2];
	}
}

spandora.SongServerManager = class {
    constructor() {

    }

    getQueue() {
        return new Promise((resolve, reject) => {
            fetch(apiUrl + "queue/")
            .then((response) => response.json())
            .then((data) => {
                resolve(data);
            })
            .catch(err => {
                reject(err);
            });
        });
    }

    getSongs() {
        return new Promise((resolve, reject) => {
            fetch(apiUrl + "songlist/")
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                resolve(data);
            })
            .catch(err => {
                reject(err);
            });
        });
    }

    addToQueue(songID) {
        return new Promise((resolve, reject) => {
            let data = {songID};
            fetch(apiUrl + "insert/", {
                method: "POST",
			    headers: {"Content-Type": "application/json"},
			    body: JSON.stringify(data)
            })
            .then((response) => {
                console.log("Song added to queue.");
                resolve(data);
            })
            .catch(err => {
                reject(err);
            });
        });
    }

    uploadSong() {
        let formData = new FormData(); 
        let fileupload = document.querySelector("#fileupload");
        formData.append("file", fileupload.files[0]);
        const fetchOptions = {
            method: "POST",
            body: formData,
        };

        fetch(apiUrl + "create/", fetchOptions)
        .then((response) => {
            console.log("Successfully uploaded file.")
        })
        .catch(err => {
            console.log("File upload failed.");
        });
    }

    playSong() {
        fetch(apiUrl + "play/")
        .then((response) => {
            console.log("Song started playing.");
        });
    }

    pauseSong() {
        fetch(apiUrl + "pause/")
        .then((response) => {
            console.log("Paused song.");
        });
    }

    resumeSong() {
        fetch(apiUrl + "resume/")
        .then((response) => {
            console.log("Resumed song.");
        });
    }

    skipSong() {
        fetch(apiUrl + "stop/")
        .then((response) => {
            fetch(apiUrl + "play/")
            .then((response) => {
                console.log("Skipped to next song.");
            });
        });
    }
}

/* Main to start everything */
spandora.main = function () {
    console.log("Ready");
    spandora.songServerManager = new spandora.SongServerManager();
    spandora.pageController = new spandora.PageController(); 

};

spandora.main();