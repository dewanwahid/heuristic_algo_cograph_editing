def get_partitions(P: list, S: list):
    if len(P) == 0:
        P.append(S)
    else:
        for p in P:
            for e in S:
                if e in p:
                    S = p + S
                    P.remove(p)
                    S = list(dict.fromkeys(S))
                    break

        P.append(S)
    return P


if __name__ == '__main__':
    P = [[1, 2, 3], [4, 5, 6]]
    S = [2, 7]
    Px = get_partitions(P, S)
    print(Px)
