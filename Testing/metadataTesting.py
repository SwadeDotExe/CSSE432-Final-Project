import audio_metadata

# Library link: https://pypi.org/project/audio-metadata/

metadata = audio_metadata.load('FinalProject/AudioFiles/JC Overture.mp3')

# Print all metadata
# print(metadata)

# Save metadata to variables
artist = metadata['tags']['artist'][0]
album = metadata['tags']['album'][0]
title = metadata['tags']['title'][0]
duration = metadata['streaminfo']['duration']

# Print metadata of interest
print(artist)
print(album)
print(title)
print(duration)
