import json


def main():
    file = open('../../dataset/movie_reviews/movies_pretty.json')
    data = json.load(file)
    trec_titles = {}
    for d in data:
        values = data[d]
        trec_titles[d] = 0
        print(values)
    file.close()

    file = open('../../dataset/movie_reviews/movie_reviews.json')
    reviews = {}
    for line in file:
        data = json.loads(line)
        id = data['imdbid']
        if id in trec_titles :
            if id in reviews :
                reviews[id].append(data)
            else :
                reviews[id] = [data]
        print(data)
    file.close()

    file = open('../../dataset/movie_reviews/movies_pretty.json')
    data = json.load(file)
    new_data = {}
    for d in data:
        values = data[d]
        if d in reviews :
            values['Reviews'] = reviews[d]
        else :
            values['Reviews'] = []
        new_data[d] = values
        print(f'Added {d}')
    file.close()
    file_out = open('../../dataset/movie_reviews/pretty_movie_data.json', 'w')
    json.dump(new_data, file_out)

if __name__ == "__main__":
    main()
