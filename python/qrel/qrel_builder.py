import re
import json


def main():
    print('Loading json file...')
    file = open('../../dataset/movie_reviews.json')
    json_object = json.load(file)
    qrels_to_add = {}
    while len(qrels_to_add) < 50 :
        print('Enter a movie title:')
        title = str(input()).lower()
        ids = listOfKeys = [key  for (key, value) in json_object.items() if title in value['Title'].lower()]
        results = []
        for id in ids :
            if id not in qrels_to_add and id:
                results.append([json_object[id]['Title'], id])
        for movie in results:
            print(f'Is "{movie[0]}" relevant to query? (y/n)')
            answer = str(input()).lower()
            if answer == 'y' :
                qrels_to_add[movie[1]] = 1
            else :
                qrels_to_add[movie[1]] = 0

    print('\n Now building qrels file...')
    qrel_file = open('../../dataset/movies.qrels', 'w')
    for q in qrels_to_add :
        qrel_file.write(f'{1} 0 {q} {qrels_to_add[q]}\n')

    print('\n Complete')


if __name__ == '__main__':
    main()
