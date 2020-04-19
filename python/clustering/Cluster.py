import math
import random
import imp
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from clustering.Word2Vec import vectorize
import numpy as np


def k_means_pp(data, k, visualize=False, d=2):
    point_data = json_to_matrix(data)
    movie_id_index = 2
    if visualize:
        parse_data = [[] for i in range(len(point_data))]
        movie_ids = []
        for point in range(len(point_data)):
            row = []
            for column in point_data[point]:
                if type(column) == str:
                    movie_ids.append(column)
                else:
                    row.append(column)
            pca = PCA(n_components=1)
            pca.fit(row)
            v_row = pca.transform(row)
            ex_v_row = []
            for item in v_row:
                ex_v_row.append(item[0])
            parse_data[point] = ex_v_row

        # print(parse_data)
        pca = PCA(n_components=d)
        pca.fit(parse_data)
        point_data = pca.transform(parse_data)
        point_data = [list(i) for i in point_data]
        for point in range(len(point_data)):
            point_data[point].append(movie_ids[point])
        movie_id_index = 1

    centers = []
    centers.append(point_data[0])
    mean_costs = []
    for i in range(1, k):
        V = 0.0
        distances = []
        sum = 0.0
        for point in point_data:
            min = math.inf
            for curr_center in centers:
                curr_distance = euclidean_distance(point[:len(point)-movie_id_index], curr_center)
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
            curr_distance = euclidean_distance(point[:len(point)-movie_id_index], curr_center)
            if curr_distance < min:
                min = curr_distance
        sum += min ** 2
    mean_costs.append(math.sqrt(sum / len(point_data)))
    json_data, clusters = find_nearest_centers(point_data, data, centers, k)
    if visualize:
        plot_clusters(clusters)
    return json_data


def plot_clusters(data):
    colors = ['#fa675c', '#2fc9f7', '#00c41a', '#bc1fff', '#ff931f']
    for cluster in range(len(data)):
        x = []
        y = []
        for point in range(len(data[cluster])):
            curr_point = data[cluster][point]
            x.append(curr_point[0])
            y.append(curr_point[1])
        plt.scatter(x, y, c=[colors[cluster]], alpha=0.5, label=f'Cluster {cluster + 1}')
    plt.title("Post query movie groupings")
    # plt.show()
    plt.savefig('post_query_movie_groupings.jpg')


def find_nearest_centers(point_data, json_data, centers, k=3):
    clusters = [[] for i in range(k)]
    for point in point_data:
        min = math.inf
        center = 0
        for i in range(len(centers)):
            curr_distance = euclidean_distance(point[:len(point)-1], centers[i])
            if curr_distance < min:
                min = curr_distance
                center = i
        clusters[center].append(point)
    for cluster in range(len(clusters)-1):
        for point in clusters[cluster]:
            movieID = point[len(point)-1]
            json_data[movieID]["Cluster"] = cluster
    return json_data, clusters


def euclidean_distance(point1, point2):
    sum = 0
    if len(point1) > 2:
        for point in range(len(point1)):
            diff = (point1[point] - point2[point])**2
            for p in diff:
                sum += p
    else:
        for point in range(len(point1)):
            diff = (point1[point] - point2[point])**2
            sum += diff
    return math.sqrt(sum)

def json_to_matrix(json_data):
    data = []
    for movie in json_data:
        row = []
        description = json_data[movie]['Description'].split() if len(json_data[movie]['Description']) > 0 else [" "]
        title = json_data[movie]['Title'].split() if len(json_data[movie]['Title']) > 0 else [" "]
        actors = json_data[movie]['Actors'].split(',') if len(json_data[movie]['Actors']) > 0 else [" "]
        director = json_data[movie]['Director'].split(',') if len(json_data[movie]['Director']) > 0 else [" "]
        writer = json_data[movie]['Writer'].split(',') if len(json_data[movie]['Writer']) > 0 else [" "]
        prod_company = [json_data[movie]['Production Company']] if len(json_data[movie]['Production Company']) > 0 else [" "]
        genre = json_data[movie]['Genre'].split() if len(json_data[movie]['Genre']) > 0 else [" "]
        avg_vote = [json_data[movie]['Avg Vote']] if len(json_data[movie]['Avg Vote']) > 0 else [" "]

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
