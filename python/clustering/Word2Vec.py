from gensim.models import Word2Vec
import numpy as np

def vectorize(data):
    model = Word2Vec(data, size=100, min_count=1)
    average_tweet_vectors = []
    for data_i in data:
        average_vector = get_average_vector(data_i, model)
        average_tweet_vectors.append(average_vector)
    print(average_tweet_vectors)
    return average_tweet_vectors

def get_average_vector(tweet, model):
    average_vector = []
    num_tokens = 0
    for token in tweet:
        try:
            if num_tokens == 0:
                average_vector = model[token]
            else:
                average_vector = np.add(average_vector, model[token])
            num_tokens += 1
        except:
            pass
    return np.asarray(average_vector) / num_tokens