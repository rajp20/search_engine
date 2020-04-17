import json
import csv
import re

def main():
    csv_file = open('../../dataset/IMDb/imdb-extensive-dataset/IMDb movies.csv')
    csv_reader = csv.reader(csv_file)
    trec_titles = {}
    next(csv_reader)
    for row in csv_reader :
        print(row[1])
        trec_titles[row[1]] = str(re.search(r'\d+', row[0]).group())
    csv_file.close()

    file = open('../../dataset/movie_reviews/meta_Movies_and_TV.json')
    movie_titles = {}
    for line in file:
        data = json.loads(line)
        if 'title' in data and 'asin' in data:
            if 'var aPageStart' not in data['title'] and data['title'] in trec_titles:
                print('FOUND: ', data['title'], data['asin'])
                movie_titles[data['asin']] = [data['title'], trec_titles[data['title']]]
    print('\n Movie Titles added to dictionary')
    file.close()

    print('\n Starting the writing of reviews...')
    file = open('../../dataset/movie_reviews/Movies_and_TV.json')
    file_out = open('../../dataset/movie_reviews/movie_reviews.json', 'w')
    count = 0
    for line in file:
        data = json.loads(line)
        if data['asin'] in movie_titles :
            data['title'] = movie_titles[data['asin']][0]
            data['imdbid'] = movie_titles[data['asin']][1]
            count += 1
            json_data = json.dumps(data)
            file_out.write(f'{json_data}\n')
            print(data)
    print('\n DONE.')
    print(f'\nCreated {count} reviews on {len(movie_titles)} movies.')



if __name__ == "__main__":
    main()
