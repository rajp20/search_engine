import json


def main():
    file = open('../../dataset/movie_reviews/pretty_movie_data.json')
    data = json.load(file)
    for d in data:
        values = data[d]
        if len(values['Reviews']) != 0 :
            review_dict = values['Reviews']
            for r in review_dict :
                print('yo')
        print(len(values['Reviews']))
    file.close()

if __name__ == "__main__":
    main()
