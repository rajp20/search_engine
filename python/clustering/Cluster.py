import math
import random

data=None

def k_means_pp(string):
#     print(data)
    for item in data:
        print(item)
    # centers = []
    # centers.append(data[0])
    # mean_costs = []
    # for i in range(1, k):
    #     V = 0.0
    #     distances = []
    #     sum = 0.0
    #     for point in data:
    #         min = math.inf
    #         for curr_center in centers:
    #             curr_distance = euclidean_distance(point, curr_center)
    #             if curr_distance < min:
    #                 min = curr_distance
    #         sum += min ** 2
    #         V += min ** 2
    #         distances.append(min ** 2)
    #     mean_costs.append(math.sqrt(sum / len(data)))
    #     accumulator = 0.0
    #     random_prob = random.random()
    #     for point_index in range(len(data)):
    #         accumulator += distances[point_index] / V
    #         if accumulator > random_prob:
    #             centers.append(data[point_index])
    #             break
    # sum = 0.0
    # for point in data:
    #     min = math.inf
    #     for curr_center in centers:
    #         curr_distance = euclidean_distance(point, curr_center)
    #         if curr_distance < min:
    #             min = curr_distance
    #     sum += min ** 2
    # mean_costs.append(math.sqrt(sum / len(data)))
    # return centers, mean_costs

def euclidean_distance(point1, point2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(point1, point2)]))