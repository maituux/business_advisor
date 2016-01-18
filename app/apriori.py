import sys
import os.path
import csv
import math 
import types
from collections import defaultdict, Iterable
import itertools
#sys.path.append("C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test")
from app import connection, transform
from app.connection import db
from flask import session
"""
sys.path.append('/Users/utilisateur/Desktop/gitBA/business_advisor/')
import app
from app import app
"""
import pymongo
from pymongo import MongoClient
import logging

class Apriori:
    def __init__(self, data, minSup, minConf):
        self.dataset = data
        self.transList = defaultdict(list)
        self.freqList = defaultdict(int)
        self.itemset = set()
        self.highSupportList = list()
        self.numItems = 0
        self.prepData()             # initialize the above collections

        self.F = defaultdict(list)

        self.minSup = minSup
        self.minConf = minConf

    def genAssociations(self):
        candidate = {}
        count = {}

        self.F[1] = self.firstPass(self.freqList, 1)
        k=2
        while len(self.F[k-1]) != 0:
            candidate[k] = self.candidateGen(self.F[k-1], k)
            for t in self.transList.iteritems():
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        self.freqList[c] += 1

            self.F[k] = self.prune(candidate[k], k)
            if k > 2:
                self.removeSkyline(k, k-1)
            k += 1

        return self.F

    def removeSkyline(self, k, kPrev):
        for item in self.F[k]:
            subsets = self.genSubsets(item)
            for subset in subsets:
                if subset in (self.F[kPrev]):
                    self.F[kPrev].remove(subset)
                    

        subsets = self.genSubsets

    def prune(self, items, k):
        f = []
        for item in items:
            count = self.freqList[item]
            support = self.support(count)
            if support >= .95:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    def candidateGen(self, items, k):
        candidate = []

        if k == 2:
            candidate = [tuple(sorted([x, y])) for x in items for y in items if len((x, y)) == k and x != y]
        else:
            candidate = [tuple(set(x).union(y)) for x in items for y in items if len(set(x).union(y)) == k and x != y]
        
        for c in candidate:
            subsets = self.genSubsets(c)
            if any([ x not in items for x in subsets ]):
                candidate.remove(c)

        return set(candidate)

    def genSubsets(self, item):
        subsets = []
        for i in range(1,len(item)):
            subsets.extend(itertools.combinations(item, i))
        return subsets

    def genRules(self, F):
        H = []

        for k, itemset in F.iteritems():
            if k >= 2:
                for item in itemset:
                    subsets = self.genSubsets(item)
                    for subset in subsets:
                        if len(subset) == 1:
                            subCount = self.freqList[subset[0]]
                        else:
                            subCount = self.freqList[subset]
                        itemCount = self.freqList[item]
                        if subCount != 0:
                            confidence = self.confidence(subCount, itemCount)
                            if confidence >= self.minConf:
                                support = self.support(self.freqList[item])
                                rhs = self.difference(item, subset)
                                if len(rhs) == 1:
                                    H.append((subset, rhs, support, confidence))

        return H

    def difference(self, item, subset):
        return tuple(x for x in item if x not in subset)

    def confidence(self, subCount, itemCount):
        return float(itemCount)/subCount

    def support(self, count):
        return float(count)/self.numItems

    def firstPass(self, items, k):
        f = []
        for item, count in items.iteritems():
            support = self.support(count)
            if support == 1:
                self.highSupportList.append(item)
            elif support >= self.minSup:
                f.append(item)

        return f

    """
    Prepare the transaction data into a dictionary
    key: Receipt.id
    val: set(Goods.Id) 

    Also generates the frequent itemlist for itemsets of size 1
    key: Goods.Id
    val: frequency of Goods.Id in self.transList
    """
    def prepData(self):
        key = 0
        for basket in self.dataset:
            self.numItems += 1
            key = basket[0]
            for i, item in enumerate(basket):
                if i != 0:
                    self.transList[key].append(item.strip())
                    self.itemset.add(item.strip())
                    self.freqList[(item.strip())] += 1

def mainAlgorithm(inputFilename):
    ######## Connection to the customer collection
    # get the name of the customer collection using the session 
    #collectionName = 'Customer_568d3b7222c8e507363c1f6f'
    
    collectionName = 'Customer_'+session['userId']
    #print (collectionName)
    #download the customer collection
    customerDB = connection.get_collection(collectionName)
    #print (customerDB)
    # INIT PARAMETERS before running the Apriori Algorithm
    #prepare the transactional data in a csv file (apriori_data.csv) 
    # logging.basicConfig(format='%(asctime)s %(message)s')
    # logging.warning('is when the input data transformation is called.')
    transform.prepare_data(customerDB)
    filename = 'apriori_data.csv'

    #access to the customer rules collection where the rules will be stored
    rulesDB=customerDB['Rules']
    #print(rulesDB)

    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.warning('is when the running of the data mining Apriori Algorithm is starting.')

    goods = defaultdict(list)
    num_args = 3
    minSup = minConf = 0
    noRules = False

    # Make sure the right number of input files are specified
    #print sys.path  

    dataset = csv.reader(open(filename, "r"))
    goodsData = csv.reader(open(inputFilename, "r"))
    # minSup  = aMinSup
    minSup = 0.2
    # minConf = aMinConf
    minConf = 0.7
    
    csvfile = open('rules.csv', 'wb') 
    writer = csv.writer(csvfile, delimiter=' ')

    print "Dataset: ", filename, " MinSup: ", minSup, " MinConf: ", minConf

    row= "Dataset: "+ filename+ " MinSup: "+ str(minSup)+ " MinConf: "+ str(minConf)
    writer.writerow(row)

    print "=================================================================="
    row= "=================================================================="
    writer.writerow(row)
    for item in goodsData:
        goods[item[0]] = item[1:]

    a = Apriori(dataset, minSup, minConf)

    frequentItemsets = a.genAssociations()

    count = 0
    for k, item in frequentItemsets.iteritems():
        for i in item:
            if k >= 2:
                count += 1
                print(str(count)+":  "+readable(i, goods)+"\tsupport=",a.support(a.freqList[i]))

    print "Skyline Itemsets: ", count
    if not noRules:
        rules = a.genRules(frequentItemsets)
        for i, rule in enumerate(rules):
            print "Rule",i+1,":\t ",readable(rule[0], goods),"\t-->",readable(rule[1], goods),"\t [sup=",rule[2]," conf=",rule[3],"]"

            row= "Rule",i+1,":\t ",readable(rule[0], goods),"\t-->",readable(rule[1], goods),"\t [sup=",rule[2]," conf=",rule[3],"]"
            writer.writerow(row)


            newRule = {"rule number": i+1, "explained product":readable(rule[0], goods), "explaining product": readable(rule[1], goods), "support": rule[2], "confidence":rule[3]}
            ruleid = rulesDB.insert(newRule)
            print (str(ruleid))

    print "\n"
    csvfile.close()

    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.warning('is when the running of the data mining Apriori Algorithm ends.')


def readable(item, goods):
    itemStr = ''
    for k, i in enumerate(item):
        itemStr += goods[i][0] + " " + goods[i][1] +" (" + i + ")"
        if len(item) != 0 and k != len(item)-1:
            itemStr += ",\t"

    return itemStr.replace("'", "")

