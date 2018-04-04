# Coconut

DataMining Course project @CentraleSupelec.

This projects aims to do music recommendation based one similar people tastes without any central server knowing the tastes or personnal data of each individual.

## Installing the projects
Just do
```
pip install -r requirements.txt
```

## Scrapping the audio files (`scrapper.py`)
`ROOT_DIR_PATH` variable is the root music directory filepath
The root folder must be ordered like : Root/ArtistFolder/AlbumFolder/MusicFile.
Amarok or Clementine should be used daily in order to generate enough listenning stats in order to have good reccomentations.

The following files are accepted : *.ogg*, *.flac*, *.mp3*
The metadata of the collections is then exported to the file `data/track_collection.json`.

## Lauch
```
python main.py
```
