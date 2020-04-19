import math
import random
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from clustering.Word2Vec import vectorize


def k_means_pp(data, k, visualize=False, d=2):
    point_data = json_to_matrix(data)
    movie_id_index = 2
    k = k if len(data) > k else len(data)
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
                curr_distance = euclidean_distance(point[:len(point) - movie_id_index], curr_center)
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
            curr_distance = euclidean_distance(point[:len(point) - movie_id_index], curr_center)
            if curr_distance < min:
                min = curr_distance
        sum += min ** 2
    mean_costs.append(math.sqrt(sum / len(point_data)))
    json_data, clusters = find_nearest_centers(point_data, data, centers, k)
    if visualize:
        plot_clusters(clusters, centers)
    return json_data


def plot_clusters(data, centers):
    colors = ['#fa675c', '#2fc9f7', '#00c41a', '#bc1fff', '#ff931f']
    for cluster in range(len(data)):
        x = []
        y = []
        for point in range(len(data[cluster])):
            curr_point = data[cluster][point]
            x.append(curr_point[0])
            y.append(curr_point[1])
        plt.scatter(x, y, c=[colors[cluster]], alpha=0.5, label=f'Cluster {cluster + 1}')

    x = [i[0] for i in centers]
    y = [i[1] for i in centers]
    plt.scatter(x, y, c='black', alpha=1.0, label="Centers")

    plt.title("Post query movie groupings")
    plt.legend()
    # plt.show()
    plt.savefig('post_query_movie_groupings')


def find_nearest_centers(point_data, json_data, centers, k=3):
    clusters = [[] for i in range(k)]
    for point in point_data:
        min = math.inf
        center = 0
        for i in range(len(centers)):
            curr_distance = euclidean_distance(point[:len(point) - 1], centers[i])
            if curr_distance < min:
                min = curr_distance
                center = i
        clusters[center].append(point)
    for cluster in range(len(clusters)):
        for point in clusters[cluster]:
            movieID = point[len(point) - 1]
            json_data[movieID]["Cluster"] = cluster
    return json_data, clusters


def misra_gries(json_data, k=10):
    # build terms for each cluster
    cluster_data = {}
    for data in json_data:
        movie_point = json_data[data]
        genre = movie_point['Genre'].split()
        if movie_point['Cluster'] in cluster_data:
            cluster_data[movie_point['Cluster']].extend(genre)
        else:
            cluster_data[movie_point['Cluster']] = genre

    # perform Misra Gries
    frequent_terms = {}
    for cluster in cluster_data:
        A = cluster_data[cluster]
        C = [0] * (k - 1)
        L = {}
        for i in range(len(A)):
            key = [key for (key, value) in L.items() if value == A[i]]
            if len(key) == 1:
                C[key[0]] += 1
            elif 0 in C:
                index = C.index(0)
                L[index] = A[i]
                C[index] = 1
            else:
                for j in range(0, k - 1):
                    C[j] -= 1
                    if C[j] < 0:
                        C[j] = 0
        # sort the terms
        sorted_arr = []
        for i in range(len(C)):
            if i in L.keys():
                sorted_arr.append([C[i], L[i]])
        sorted_arr.sort(key=lambda x: x[0], reverse=True)
        frequent_terms[cluster] = sorted_arr

    # Now add the terms to the json data and return it
    for data in json_data:
        movie_point = json_data[data]
        json_data[data]['Frequent Terms'] = [genre[1] for genre in frequent_terms[movie_point['Cluster']]]
    return json_data



def euclidean_distance(point1, point2):
    sum = 0
    if len(point1) > 2:
        for point in range(len(point1)):
            diff = (point1[point] - point2[point]) ** 2
            for p in diff:
                sum += p
    else:
        for point in range(len(point1)):
            diff = (point1[point] - point2[point]) ** 2
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
        prod_company = [json_data[movie]['Production Company']] if len(
            json_data[movie]['Production Company']) > 0 else [" "]
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
