from getlinks import main as download
from filter import main as filter
import time

download(movie_url="https://filman.cc/serial-online/853/rekrut-the-rookie", 
         minSeason=6, maxSeason=6, minEpisode=8)
print("Filtering")
filter(isnapisy_transl=True)
