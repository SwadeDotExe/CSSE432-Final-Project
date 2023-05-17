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
const apiUrl = window.location.href + "/api/";
spandora.pageController = null;
spandora.songServerManager = null;

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

        // Adding songs to queue
		document.querySelector("#submitSongToQueue").addEventListener("click", (event) => {
			spandora.songServerManager.addToQueue(this._searchedSongID);
		})

        this.initializeView();
    }

    initializeView() {
        // this.updateQueue();
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
        const newQueue = htmlToElement(`<div id="queueListContainer"></div>`);
		for (let i = 0; i < fullQueueList.length; i++) {
            // Get item from json
            const song = new Song(data[i]);
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
            this._testUpdateSongList(data)
        })
        .catch(err => {
			console.log(err);
		});
	}

    _testUpdateSongList(data) {
        let fullSongList = data;
        for (let i = 0; i < fullSongList.length; i++) {
            let stringData = fullSongList[i].split("_");
            const song = new Song(stringData);
            console.log(song);
        }
    }

    _updateSongListHelper(data) {
        let fullSongsList = data;
        const newSongList = htmlToElement(`<div id="songListContainer"></div>`);
        for (let i = 0; i < fullSongsList.length; i++) {
            // Get item from json as a song
            const song = new Song(fullSongsList[i]);
            const newSong = spandora.pageController._createListedSong(song);
            newSong.onclick = (event) => {
				this._searchedSongID = newSong.id;
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
spandora.Song = class {
	constructor(songData) {
		this.songName = songData[0];
        this.id = songData[1];
		this.artist = songData[2];
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
        let data = {songID};
        fetch(apiUrl + "insert/", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(data)
		})
		.catch (err => {
			console.log(err);
		})
    }

    addSongToServer() {

    }
}

/* Main to start everything */
spandora.main = function () {
    console.log("Ready");
    spandora.songServerManager = new spandora.SongServerManager();
    spandora.pageController = new spandora.PageController(); 

};

spandora.main();