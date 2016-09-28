import sys
from prettytable import PrettyTable
import itertools

class Apriori(object):

    def __init__(self, database = [], threshold = 2, print_sol = False, print_steps = False):
        self.database = database
        self.threshold = threshold
        if print_sol:
            self.print_sol = True
        else:
            self.print_sol = False

        self.solution = []
        self.solution_count = []

        if print_steps:
            self.print_steps = True
        else:
            self.print_steps = False


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
        print('***** Printing Final Solutions *****')

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

    def generate_solution_one(self):
        self.solution.append(self.one_itemsets(self.database))

        if self.print_steps:
            pt = PrettyTable()
            pt.add_column('Itemsets', self.solution[0])
            print("\nFound candidates C_%d:\n%s\n" % (1, pt))

        count = [0 for _ in range(0,len(self.solution[0]))]

        for transaction in self.database:
            subset_count = self.count_subsets(self.solution[0], transaction)

            i = 0
            for c in subset_count:
                count[i] += c
                i += 1

        i = 0
        for itemset in self.solution[0]:
            if count[i] < self.threshold:
                del count[i]
                del self.solution[0][i]
            i += 1


        self.solution_count.append(count)


    def run(self):
        self.generate_solution_one()

        k = 2

        while self.solution[k-2]:
            candidates = self.generate_candidates(self.solution[k-2], k)

            count = [0 for _ in range(0,len(candidates))]

            if self.print_steps:
                pt = PrettyTable()
                pt.add_column('Itemsets', candidates)
                print("\nFound candidates C_%d:\n%s\n" % (k, pt))

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
                    self.solution[k-1].append(c)
                    self.solution_count[k-1].append(count[key])
                else:
                    print('Pruned %s since %d < %d' % (c, count[key], self.threshold))
                key += 1
            k += 1

        # if pretty print:
        if self.print_sol == True:
            self.print_solution()


if len(sys.argv) < 2:
    pass

database = [['a','b','e'],['b','d'],['c','d','f'],['a','b','d'],['a','c','e'],['b','c','e','f'],['a','c','e'],['a','b','c','e'],['a','b','c','d','f'],['b','c','d','e']]

#database = [['a','b','e'],['b','d'],['c','d'],['a','b','d'],['a','c','e'],['b','c','e'],['a','c','e'],['a','b','c','e'],['a','b','c','d','f'],['b','c','d','e']]

apriori = Apriori(database, 2, True, True)
apriori.run()
