import csv
import pathlib
import pickle

namesDic = {}
movie_dir = pathlib.Path('/opt/movies')

with open('halloweenMovies.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar=';')
    for row in spamreader:
        print(row)
        namesDic[row[0]] = [[int(x) for x in row[1].strip('] [').split(',')]]
    for name in namesDic.keys():
        for path in movie_dir.glob(f'**/*{name}*.mkv'):
            namesDic[name].append(path)
with open('MoviePickle.pickle', 'wb') as handle:
    pickle.dump(namesDic, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(namesDic)
