import math
import random
import imp
from clustering.Word2Vec import vectorize

def k_means_pp(data, k):
    data = json_to_matrix(data)

    centers = []
    centers.append(data[0])
    mean_costs = []
    for i in range(1, k):
        V = 0.0
        distances = []
        sum = 0.0
        for point in data:
            min = math.inf
            for curr_center in centers:
                curr_distance = euclidean_distance(point, curr_center)
                if curr_distance < min:
                    min = curr_distance
            sum += min ** 2
            V += min ** 2
            distances.append(min ** 2)
        mean_costs.append(math.sqrt(sum / len(data)))
        accumulator = 0.0
        random_prob = random.random()
        for point_index in range(len(data)):
            accumulator += distances[point_index] / V
            if accumulator > random_prob:
                centers.append(data[point_index])
                break
    sum = 0.0
    for point in data:
        min = math.inf
        for curr_center in centers:
            curr_distance = euclidean_distance(point, curr_center)
            if curr_distance < min:
                min = curr_distance
        sum += min ** 2
    mean_costs.append(math.sqrt(sum / len(data)))
    return centers, mean_costs

def euclidean_distance(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))

def json_to_matrix(json_data):
    data = []
    for movie in json_data:
        description = json_data[movie]['Description'].split()
        title = json_data[movie]['Title'].split()
        actors = json_data[movie]['Actors'].split(',')
        director = json_data[movie]['Director'].split(',')
        writer = json_data[movie]['Writer'].split(',')
        prod_company = [json_data[movie]['Production Company']]
        genre = json_data[movie]['Genre'].split()
        avg_vote = float([json_data[movie]['Avg Vote']])

        data.append(description)
        data.append(title)
        data.append(actors)
        data.append(director)
        data.append(writer)
        data.append(prod_company)
        data.append(genre)
        data.append(avg_vote)

        data = vectorize(data)
        data.append(avg_vote)

        return data