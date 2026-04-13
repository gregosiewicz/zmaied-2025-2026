import random
import matplotlib.pyplot as plt

def dist(p, q):
    return sum((pp - qq) ** 2 for pp, qq in zip(p, q))

# p = [p0, p1, p2, ..., pn]
# q = [q0, q1, q2, ..., qn]

# zip(p, q) = [[p0, q0], [p1, q1], ..., [pn, qn] ]
# zip(p, q) = [ p0 p1 p2 ... pn ]
#             [ q0 q1 q2 ... qn ]

# def f(a, b, c):
#     return a + b + c

# d = (1, 2, 3)
# print(f(*d))

def center(points):
    return [sum(coords) / len(points) for coords in zip(*points)]


def assign(points, centroids):
    assignments = []
    for p in points:
        dists = [dist(p, c) for c in centroids]
        assignments.append(dists.index(min(dists))) # argmin
    return assignments


def kmeans(points, k, max_iter=100, eps=1e-3):
    centroids = random.sample(points, k)

    for _ in range(max_iter):
        assignments = assign(points, centroids)
        clusters = [[] for _ in range(k)]
        for i, p in enumerate(points):
            clusters[assignments[i]].append(p)
        
        new_centroids = [center(cluster) for cluster in clusters]

        if max(dist(center, new_center) for center, new_center in zip(centroids, new_centroids)) < eps:
            break

        centroids = new_centroids

    return clusters, centroids


def generate_random_points(
    n_centers=3,
    n_points_in_centers=200,
    spread=0.4,
):
    centers = [
        [random.uniform(-5, 5), random.uniform(-5, 5)]
        for _ in range(n_centers)
    ]

    points = []
    for cx, cy in centers:
        for _ in range(n_points_in_centers):
            points.append(
                [
                    random.gauss(cx, spread),
                    random.gauss(cy, spread),
                ]
            )

    return points

def plot_points(points):
    xs, ys = zip(*points)
    plt.scatter(xs, ys, c="gray", alpha=0.6, s=80)
    plt.tight_layout()
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    plt.close()

colors = ["red", "blue", "green", "purple", "cyan", "orange"]

def plot_clusters(clusters, centroids):
    for i, c in enumerate(clusters):
        xs, ys = zip(*c)
        plt.scatter(xs, ys, c=colors[i % len(colors)], alpha=0.6, s=80)
    xs, ys = zip(*centroids)
    plt.scatter(xs, ys, c="black", s=150, marker="X")
    plt.tight_layout()
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    plt.close()

points = generate_random_points(n_centers=1, n_points_in_centers=10000, spread=1)
plot_points(points)
clusters, centroids = kmeans(points, 8)
plot_clusters(clusters, centroids)
