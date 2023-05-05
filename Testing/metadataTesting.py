import audio_metadata

# Library link: https://pypi.org/project/audio-metadata/

metadata = audio_metadata.load('FinalProject/AudioFiles/JC Overture.mp3')

# Print metadata
print(metadata)