import numpy as np
<<<<<<< HEAD:methods/dp_bitmask/dp_bitmask.py
import time
class DPBitmask:

    def __init__(self, time_limit):
        self.time_limit = time_limit

    def tsp(self, mask, pos, number):
=======

class Bruteforce:

    def tsp(self,mask, pos, number):
>>>>>>> 87e8c8452e23ad143a0327e470908f6f2655d856:methods/brute force/brute_force.py
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

    def solve(self,instance):
        self.sub_dist = []
        self.dp = []
        dist = instance.data["distance_matrix"]
        k = instance.data["K"]
        n = len(dist[0]) - 1
<<<<<<< HEAD:methods/dp_bitmask/dp_bitmask.py
        self.sub_dist = []
        self.dp = []
        log = []
        cur = k ** n

        a = []

        for i in range(n+1):
            listt = [0 for x in range(n+1)]
            self.sub_dist.append(listt)

=======
        cur = k ** n

        a = []
            
>>>>>>> 87e8c8452e23ad143a0327e470908f6f2655d856:methods/brute force/brute_force.py
        ans =  1e9

        self.sub_dist = [[0 for x in range(n+1)] for y in range(n+1)]

        for i in range(cur):
            sub_ans = 0
            tmp = i

            a = []
            self.dp = []

            for j in range(1,k+2):
                a.append([0])
            

            for j in range(1,n+1):
                a[tmp % k + 1].append(j)
                tmp = (int)(tmp/k)

<<<<<<< HEAD:methods/dp_bitmask/dp_bitmask.py
            for j in range(1,n+1):
                for u in range(n+1):
                    list = [-1 for x in range(n+1)]
                    self.dp.append(list)
=======
            for j in range(1,k+1):
                self.dp = [[-1 for x in range(n+1)] for y in range(1<<(n+1))]
>>>>>>> 87e8c8452e23ad143a0327e470908f6f2655d856:methods/brute force/brute_force.py

                num = len(a[j])

                for u in range(num):
                    for v in range(num):
                        if (u == v): self.sub_dist[u][v] = 0
                        else: self.sub_dist[u][v] = dist[a[j][u]][a[j][v]]
                
                sub_ans = max(sub_ans, tsp(1,0,num))

                if (sub_ans > ans): break
            
            ans = min(sub_ans,ans)
<<<<<<< HEAD:methods/dp_bitmask/dp_bitmask.py
            log.append(ans)
        return ans,log
=======

        print(ans)







    
    


>>>>>>> 87e8c8452e23ad143a0327e470908f6f2655d856:methods/brute force/brute_force.py
