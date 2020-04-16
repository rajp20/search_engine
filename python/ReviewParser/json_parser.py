import json
def main():
    file = open('../../dataset/movie_reviews/meta_Movies_and_TV.json')
    movie_titles = {}
    for line in file:
        data = json.loads(line)
        if 'title' in data and 'asin' in data:
            if 'var aPageStart' not in data['title']:
                print(data['title'], data['asin'])
                movie_titles[data['asin']] = data['title']
    print('\n Movie Titles added to dictionary')
    file.close()

    print('\n Starting the writing of reviews...')
    file = open('../../dataset/movie_reviews/Movies_and_TV.json')
    file_out = open('../../dataset/movie_reviews/movie_reviews.json', 'w')
    for line in file:
        data = json.loads(line)
        if data['asin'] in movie_titles :
            data['title'] = movie_titles[data['asin']]
            file_out.write(f'{data}\n')
            print(data)
    print('\n DONE.')



if __name__ == "__main__":
    main()
