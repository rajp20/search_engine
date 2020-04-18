import math
import random
import imp
from clustering.Word2Vec import vectorize

def k_means_pp(data, k):
    point_data = json_to_matrix(data)

    centers = []
    centers.append(point_data[0][:len(point_data[0])-2])
    mean_costs = []
    for i in range(1, k):
        V = 0.0
        distances = []
        sum = 0.0
        for point in point_data:
            min = math.inf
            for curr_center in centers:
                curr_distance = euclidean_distance(point[:len(point)-2], curr_center[:len(curr_center)-2])
                if curr_distance < min:
                    min = curr_distance
            sum += min ** 2
            V += min ** 2
            distances.append(min ** 2)
        mean_costs.append(math.sqrt(sum / len(point_data)))
        accumulator = 0.0
        random_prob = random.random()
        for point_index in range(len(point_data)):
            accumulator += distances[point_index] / V
            if accumulator > random_prob:
                centers.append(point_data[point_index])
                break
    sum = 0.0
    for point in point_data:
        min = math.inf
        for curr_center in centers:
            curr_distance = euclidean_distance(point[:len(point)-2], curr_center)
            if curr_distance < min:
                min = curr_distance
        sum += min ** 2
    mean_costs.append(math.sqrt(sum / len(point_data)))
    clusters = find_nearest_centers(point_data, data, centers, k)
    return clusters

def find_nearest_centers(point_data, json_data, centers, k=3):
    clusters = [[] for i in range(k)]
    for point in point_data:
        min = math.inf
        center = 0
        for i in range(len(centers)):
            curr_distance = euclidean_distance(point, centers[i])
            if curr_distance < min:
                min = curr_distance
                center = i
        clusters[center].append(point)
    for cluster in range(len(clusters)-1):
        for point in clusters[cluster]:
            movieID = point[len(point)-1]
            json_data[movieID]["Cluster"] = cluster
    return json_data

def euclidean_distance(point1, point2):
    sum = 0
    for point in range(len(point1)-2):
        diff = (point1[point] - point2[point])**2
        for p in diff:
            sum += p
    return math.sqrt(sum)

def json_to_matrix(json_data):
    data = []
    for movie in json_data:
        row = []
        description = json_data[movie]['Description'].split()
        title = json_data[movie]['Title'].split()
        actors = json_data[movie]['Actors'].split(',')
        director = json_data[movie]['Director'].split(',')
        writer = json_data[movie]['Writer'].split(',')
        prod_company = [json_data[movie]['Production Company']]
        genre = json_data[movie]['Genre'].split()
        avg_vote = [json_data[movie]['Avg Vote']]

        row.append(description)
        row.append(title)
        row.append(actors)
        row.append(director)
        row.append(writer)
        row.append(prod_company)
        row.append(genre)
        row.append(avg_vote)
        row = vectorize(row)
        row.append(movie)
        data.append(row)

    return data