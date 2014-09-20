__author__ = 'Scott'

def median(alist):
    length = len(alist)
    if length > 0:
        sortedList = sorted(alist)
        middle = length//2
        if length%2 == 0: return (sortedList[middle-1]+sortedList[middle])/2.0
        return sortedList[middle]
    return 0
