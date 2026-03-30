from collections import defaultdict
import heapq


def func_a(n1, n2, n3):
    result = []
    temp = n1
    while temp <= n2:
        flag = True
        for i in range(2, int(temp ** 0.5) + 1):
            if temp % i == 0:
                flag = False
                break
        if flag and temp % n3 == 0:
            result.append(temp)
        temp += 1
    return result


def func_b(lst1, val1):
    lo, hi = 0, len(lst1) - 1
    idx = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst1[mid] == val1:
            idx = mid
            hi = mid - 1
        elif lst1[mid] < val1:
            lo = mid + 1
        else:
            hi = mid - 1
    return idx


def func_c(dict1):
    obj1 = defaultdict(list)
    for k, v in dict1.items():
        obj1[v].append(k)
    return {v: sorted(ks) for v, ks in obj1.items()}


def func_d(lst2):
    if len(lst2) <= 1:
        return lst2
    pivot = lst2[len(lst2) // 2]
    left = [x for x in lst2 if x[1] < pivot[1]]
    mid = [x for x in lst2 if x[1] == pivot[1]]
    right = [x for x in lst2 if x[1] > pivot[1]]
    return func_d(left) + mid + func_d(right)


def func_e(dict2, src, tgt):
    heap = [(0, src)]
    visited = {}
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited[node] = cost
        if node == tgt:
            return cost
        for neighbor, weight in dict2.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor))
    return -1


def func_f(lst3, n4):
    freq = defaultdict(int)
    for x in lst3:
        freq[x] += 1
    heap2 = []
    for val, count in freq.items():
        heapq.heappush(heap2, (count, val))
        if len(heap2) > n4:
            heapq.heappop(heap2)
    return [val for _, val in sorted(heap2, reverse=True)]


def func_g(str1):
    lookup = {}
    lo = 0
    max_len = 0
    for hi, ch in enumerate(str1):
        if ch in lookup and lookup[ch] >= lo:
            lo = lookup[ch] + 1
        lookup[ch] = hi
        max_len = max(max_len, hi - lo + 1)
    return max_len


def proc_a(data1):
    var1 = {item[0]: item[1] for item in data1}
    var2 = func_c(var1)
    var3 = [(k, len(v)) for k, v in var2.items()]
    var4 = func_d(var3)
    return var4


def proc_b(data2, num1, num2):
    var5 = func_a(num1, num2, 2)
    var6 = func_b(var5, var5[len(var5) // 2]) if var5 else -1
    var7 = func_f(data2, 3)
    return {"r1": var5, "r2": var6, "r3": var7}


def proc_c(graph1, nodes1):
    var8 = {}
    for i, src in enumerate(nodes1):
        for tgt in nodes1[i + 1:]:
            var8[(src, tgt)] = func_e(graph1, src, tgt)
    return var8


if __name__ == "__main__":
    d1 = [("x1", "g1"), ("x2", "g2"), ("x3", "g1"), ("x4", "g3"), ("x5", "g2")]
    print(proc_a(d1))

    nums = [3, 3, 1, 1, 1, 2, 2, 4]
    print(proc_b(nums, 10, 100))

    g = {
        "a": [("b", 4), ("c", 1)],
        "b": [("d", 1)],
        "c": [("b", 2), ("d", 5)],
        "d": []
    }
    print(proc_c(g, ["a", "b", "c", "d"]))

    print(func_g("arbitraryvariablenames"))
