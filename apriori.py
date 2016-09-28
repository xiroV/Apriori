import sys
from prettytable import PrettyTable
import itertools

class Apriori(object):

    def __init__(self, database = [], threshold = 2, print_sol = False):
        self.database = database
        self.threshold = threshold
        if print_sol:
            self.print_sol = True
        else:
            self.print_sol = False

        self.solution = []
        self.solution_count = []


    def one_itemsets(self, database):
        result = []

        for itemset in database:
            for item in itemset:
                if item not in result:
                    result.append(item)

        result.sort()
        return result

    def generate_candidates(self, somelist, r):
        # collect each item
        somelist = self.one_itemsets(somelist)
        return list(itertools.combinations(somelist, r))

    def count_subsets(self, candidates, transaction):
        result = []
        for cand in candidates:
            if set(cand).issubset(transaction):
                result.append(1)
            else:
                result.append(0)

        return result

    def print_solution(self):
        for i in range(0, len(self.solution)):

            print('\nPass %d' % (i+1))


            if len(self.solution[i]) > 0:
                pt = PrettyTable()

                # Transform itemset self.solution from tuple to string
                if i > 0:
                    itemsets = []
                    for j in range(0, len(self.solution[i])):
                        itemsets.append(' '.join([x for x in self.solution[i][j]]))
                else:
                    itemsets = self.solution[i]

                pt.add_column('Itemsets', itemsets)
                pt.add_column('Support', self.solution_count[i])

                print(pt)
            else:
                print("No solutions found for pass %d" % (i+1))


    def run(self):
        self.solution.append(self.one_itemsets(self.database))
        self.solution_count.append([0 for i in range(0,len(self.solution[0]))])

        k = 2

        print("S_%d: %s" % (k-1, str(self.solution[0])))


        while self.solution[k-2]:
            candidates = self.generate_candidates(self.solution[k-2], k)

            count = [0 for _ in range(0,len(candidates))]

            print("Found candidates C_%d:\n%s" % (k, candidates))

            for transaction in self.database:
                subset_count = self.count_subsets(candidates, transaction)

                i = 0
                for c in subset_count:
                    count[i] += c
                    i += 1

            key = 0
            self.solution.append([])
            self.solution_count.append([])
            for c in candidates:
                if count[key] >= self.threshold:
                    print("%s added to S_%d" % (c, k))
                    self.solution[k-1].append(c)
                    self.solution_count[k-1].append(count[key])
                key += 1
            print("S_%d: %s" % (k, str(self.solution[k-1])))
            k += 1

        # if pretty print:
        if self.print_sol == True:
            self.print_solution()


if len(sys.argv) < 2:
    pass

database = [['a','b','e'],['b','d'],['c','d','f'],['a','b','d'],['a','c','e'],['b','c','e','f'],['a','c','e'],['a','b','c','e'],['a','b','c','d','f'],['b','c','d','e']]

apriori = Apriori(database, 2, True)
apriori.run()
