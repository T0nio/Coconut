# Coconut

DataMining Course project @CentraleSupelec.

This projects aims to do music recommendation based one similar people tastes without any central server knowing the tastes or personnal data of each individual.

We created a centralized version of the algorithm we want to use, to be able to compare it with the decentralized one after. 

Our recommendation approache is to do element-element similarity based colaborative recommendation. This principle is based on the computation of a similarity matrix between all elements of the common library, to predict the rating of an unknown element.

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

## The agent system
The decentralized version is based on an agent system:
- You have one server, that knows all the users of the network. It'll orchestrate all the calculus, but will never know the data used for the calculations.
- You have n users. Each user has it's own data. A chain of users is created: it'll define the data flow. Each user knows the next user in the computation chain.

To be able to predict a score to an unknown track, each users need:
- The list of all possible tracks
- The similarity matrix between all these tracks
- It's own data vector

The server will be the master to compute the similarity matrix:
- It'll ask to the users to make the intermediate calculus
- It'll compile all these calculus to generate the similarity matrix
- Then it'll push the similarity matrix to the users

To be able to compute the similarity matrix, the server will need to know:
- The average score of each track (to normalize them after)
- The scalar product between two tracks
- The norma of each tracks

All these data are basically sums of elements for each user (sum of score, square score, or multiplication of scores). But we don't want any user to be able to know the score of another user. 
To achieve that we'll use a trick ! (yeah!) : 
- The first user of the chain will generate a huge number (thousand times bigger than the potential result), and save it
- He'll add it's own part of the calculus (score, square score, multiplication of scores) to this number
- He'll give that result to the next user, that will add it's own part of the calculus to it too
- And so on
- When the sum return to the first user (we created a closed chain, remember ?), he'll substract the huge number to the sum. And the he'll have the sum !
- After that he'll just add the last operation needed (divide by the number of users or square root for example), and give back the result to the server.

This way, we achieved to compute the similarity matrix, without giving up any row data ! 

## Project files
The two versions of the recommendation are available in two files:
- `main.py` for the centralized version of the recommendation
- `decentralized.py` for the decentralized version of the recommendation

## Notebooks 
You'll find a notebook version of the two concepts. These versions will help you to understand how the system works. 
- `DecentralizedNotebook.ipynb` for the decentralized version
- `CentralizedNotebook.ipynb` for the centralized one
