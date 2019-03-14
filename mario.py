# Ryan Alder
# March, 2019

import fileinput


# Floyd-Warshall algorithm that determines shortest distance between vertices
def floyd(g, bootarr, v, c, maxdistance):
    for i in range(v + c + 1):
        for j in range(v + c + 1):
            for k in range(v + c + 1):
                if g[j][k] > g[j][i] + g[i][k]:
                    g[j][k] = g[j][i] + g[i][k]
                    if i <= v and g[j][k] <= maxdistance:
                        bootarr[j][k] = True
                        bootarr[k][j] = True


def main():
    # rawinput is an array of all lines in user input
    rawinput = []
    inlocation = 0
    for line in fileinput.input():
        if line != '\n':
            rawinput.append(line.rstrip())

    # for each test case save paths then execute algorithm
    testcases = rawinput[0]
    for i in range(int(testcases)):
        # split by spaces, convert to int and save to local variables
        tmp = rawinput[inlocation+1].split(" ")
        villages = int(tmp[0])
        castles = int(tmp[1])
        roads = int(tmp[2])
        maxdistance = int(tmp[3])
        boots = int(tmp[4])

        # initialize undirected graph with max value roads+1
        graph = [[float("inf") for _ in range(roads+1)] for _ in range(roads+1)]
        for j in range(roads+1):
            graph[j][j] = 0

        # initialize bootarr, will be True if the boots can be used for the road
        bootarr = [[False for _ in range(roads+1)] for _ in range(roads+1)]

        # initialize dp, which will be used for the dynamic programming algorithm
        dp = [[0 for _ in range(roads+1)] for _ in range(roads+1)]

        # save the road information into the corresponding arrays
        for j in range(roads):
            tmp = list(map(int, rawinput[inlocation+j+2].split(" ")))
            graph[tmp[0]][tmp[1]] = tmp[2]
            graph[tmp[1]][tmp[0]] = tmp[2]
            if tmp[2] <= maxdistance:
                bootarr[tmp[0]][tmp[1]] = True
                bootarr[tmp[1]][tmp[0]] = True

        # update our index value
        inlocation += roads + 1

        # use Floyd-Warshall to find shortest distance between vertices
        floyd(graph, bootarr, villages, castles, maxdistance)

        # initialize the dp array with graph values
        for j in range(2, villages+castles+1):
            dp[j][0] = graph[1][j]

        # dp problem, determines where to use the boots
        changed = True
        numiter = 0
        while(changed):
            changed = False
            for j in range(2, villages+castles+1):
                for k in range(1, boots+1):
                    sol = float("inf")
                    if numiter == 0:
                        for l in range(1, j):
                            if bootarr[l][j]:
                                sol = min(sol, min(dp[l][k-1], dp[l][k] + graph[l][j]))
                            else:
                                sol = min(sol, dp[l][k] + graph[l][j])
                    else:
                        for l in range(1, villages+castles+1):
                            if bootarr[l][j]:
                                sol = min(sol, min(dp[l][k-1], dp[l][k] + graph[l][j]))
                            elif l != j:
                                sol = min(sol, dp[l][k] + graph[l][j])
                    if dp[j][k] != sol: changed = True
                    dp[j][k] = sol
            numiter += 1

        # solution to this case is found at dp[starting_point][numboots]
        print(dp[villages+castles][boots])


main()
