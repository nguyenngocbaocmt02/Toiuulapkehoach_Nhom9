import numpy as np

class DPBitmask:

    def __init__(self, sub_dist, dp):
        self.sub_dist = sub_dist
        self.dp = dp

    def tsp(self, mask, pos, number):
        if (mask == (1 << number) - 1):
            return self.sub_dist[pos][0]

        if (self.dp[mask][pos] != -1):
            return self.dp[mask][pos]

        ans = 1e9

        for city in range(number):
            if ((mask & (1 << city))): continue
            newAns = self.sub_dist[pos][city] + self.tsp(mask | (1 << city), city, number)
            ans = min(ans, newAns)

        self.dp[mask][pos] = ans
        return ans
    
    def solve(self, instance):
        dist = instance.data["distance_matrix"]
        k = instance.data["K"]
        n = len(dist[0]) - 1

        cur = k ** n

        a = []

        ans =  1e9
        for i in range(cur):
            sub_ans = 0
            tmp = i

            a.clear

            for j in range(1,k+1):
                list = [0]
                a.append(list)

            for j in range(1,n+1):
                a[tmp % k + 1].append(j)
                tmp = (int)(tmp/k)

            for j in range(1,n+1):
                for u in range(n+1):
                    list = [-1 for x in range(n)]
                    self.dp.append(list)

                num = len(a[j])

                for u in range(num):
                    for v in range(num):
                        if (u == v): self.sub_dist[u][v] = 0
                        else: self.sub_dist[u][v] = dist[a[j][u]][a[j][v]]
                    
                sub_ans = max(sub_ans, self.tsp(1,0,num))

                if (sub_ans > ans): break
            
            ans = min(sub_ans,ans)

        return ans
    




    
    


