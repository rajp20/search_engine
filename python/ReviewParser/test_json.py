import json


def main():
    file = open('../../dataset/movie_reviews/movie_reviews.json')
    for line in file:
        data = json.loads(line)
        print(data)
    file.close()


if __name__ == "__main__":
    main()
