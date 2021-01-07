# Example 1
A1 = [1, 2, 3, 3]
B1 = [2, 3, 1, 4]
N1 = 4

# Example 2
A2 = [1, 2, 4, 5]
B2 = [2, 3, 5, 6]
N2 = 6


def solution(A, B, N):
    adj = [0] * (N + 1)

    for i in range(N + 1):
        adj[i] = []

    for i in range(len(A)):
        adj[A[i]].append(B[i])
        adj[B[i]].append(A[i])

    return maxEdges(adj, N)


def maxEdges(adj, nodes):
    res = 0
    visited = [False] * (nodes + 1)

    for i in range(1, nodes + 1):

        if visited[i] == False:

            adjListSize = deepfirst(i, adj,
                                    visited, nodes)
            res = max(res, adjListSize // 2)
    return res


def deepfirst(s, adj, visited, nodes):
    adjListSize = len(adj[s])
    visited[s] = True
    for i in range(len(adj[s])):


        if visited[adj[s][i]] == False:
            adjListSize += deepfirst(adj[s][i], adj,
                                     visited, nodes)

    return adjListSize


print('Solution to Example 1 is {}'.format(solution(A1, B1, N1)))
print('Solution to Example 2 is {}'.format(solution(A2, B2, N2)))