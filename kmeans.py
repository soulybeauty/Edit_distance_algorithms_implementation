from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cost(source, target, insertion_weight=1, deletion_weight=1, substitution_weight=1, transpose_weight=1):
    if source == target:
        return 0

    n = len(source)
    m = len(target)

    # Initialize the distance matrix
    D = [[0] * (m + 1) for i in range(n + 1)]

    # Initialize the first row and column of the distance matrix
    for i in range(1, n + 1):
        D[i][0] = i * deletion_weight

    for j in range(1, m + 1):
        D[0][j] = j * insertion_weight

    # Compute the edit distance using dynamic programming
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_of_substitution = substitution_weight
            if source[i-1] == target[j-1]:
                cost_of_substitution = 0

            D[i][j] = min(D[i-1][j] + deletion_weight,
                          D[i][j-1] + insertion_weight,
                          D[i-1][j-1] + cost_of_substitution)

            # Check for transposition (combination of deletion and insertion)
            if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                transposition_cost = D[i-2][j-2] + transpose_weight
                D[i][j] = min(D[i][j], transposition_cost)

    return D[n][m]


def edit_distance_matrix(words):
    n = len(words)
    distances = [[cost(words[i], words[j]) for j in range(n)] for i in range(n)]
    return distances


def cluster_words(words, num_clusters):
    distances = edit_distance_matrix(words)

    # Perform K-means Clustering based on pairwise distances
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(distances)

    # Organize words into clusters
    cluster_dict = {}
    for i, word in enumerate(words):
        cluster_id = clusters[i]
        if cluster_id in cluster_dict:
            cluster_dict[cluster_id].append(word)
        else:
            cluster_dict[cluster_id] = [word]

    result_clusters = list(cluster_dict.values())
    return result_clusters


from utils import get_plain_vocabluary
# Example usage
word_list = ["apple", "banana", "orange", "peach", "pineapple", "grape", "pear"]
num_clusters = 200
words = get_plain_vocabluary()
result_clusters = cluster_words(words, num_clusters)
for i, cluster in enumerate(result_clusters):
    print(f"Cluster {i + 1}: {cluster}")


def evaluate_clustering(words, num_clusters):
    distances = edit_distance_matrix(words)

    # Perform K-means Clustering based on pairwise distances
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(distances)

    # Evaluate clustering using Silhouette score
    silhouette_avg = silhouette_score(distances, clusters)

    return silhouette_avg


silhouette_score = evaluate_clustering(words, num_clusters)
print("Silhouette Score:", silhouette_score)

