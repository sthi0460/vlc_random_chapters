import pickle
from random import shuffle
def gen_unique_chap_list(movie_pickle_path):
    with open(movie_pickle_path, 'rb') as handle:
        movie_dic = pickle.load(handle)

    unique_chap_list = []
    for key in movie_dic.keys():
        chapter_list = movie_dic[key][0]
        current_path = movie_dic[key][1]
        for chapter in chapter_list:
            temp_list = (key, chapter, current_path)
            unique_chap_list.append(temp_list)

    for tuple_set in unique_chap_list:
        print(tuple_set)
    print('\n\n\n_________________')
    shuffle(unique_chap_list)
    for tuple_set in unique_chap_list:
        print(tuple_set)
    with open('uniqueChapterList.pickle', 'wb') as handle:
        pickle.dump(unique_chap_list, handle,  protocol=pickle.HIGHEST_PROTOCOL)
    return unique_chap_list
