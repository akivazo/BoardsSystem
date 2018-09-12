# -*- coding: utf-8 -*-
# from appjar import gui

from util import *


class Post:
    # calculate the edges of the posts
    def _getEdges(self):
        lu = []
        lu.append(self.location[0] - self.size[0] / 2)
        lu.append(self.location[1] - self.size[1] / 2)
        ru = []
        ru.append(self.location[0] + (self.size[0]) / 2)
        ru.append(self.location[1] - (self.size[1]) / 2)
        rd = []
        rd.append(self.location[0] + (self.size[0]) / 2)
        rd.append(self.location[1] + self.size[1] / 2)
        ld = []
        ld.append(self.location[0] - self.size[0] / 2)
        ld.append(self.location[1] + self.size[1] / 2)
        return [lu, ru, rd, ld]

    def __init__(self, name, location, size, color=BLACK):
        self.name = str(name)
        self.location = location
        self.size = size
        self.edges = self._getEdges()
        self.color = color # the color of the post

    # return true if the post in the 'location' and 'size' is overlap with self
    def isPostIn(self, location, size):
        if (self.location[0] - self.size[0] / 2) > (location[0] + size[0] / 2) \
                or (self.location[1] - self.size[1] / 2) > (location[1] + size[1] / 2) \
                or (self.location[0] + self.size[0] / 2) < (location[0] - size[0] / 2) \
                or (self.location[1] + self.size[1] / 2) < (location[1] - size[1] / 2):
            return False
        return True

    # return the width of overlap of the post in the 'location' and 'size', and self.
    def getOverlapWidth(self, location, size):
        """if location[0] + size[0]/2 >= self.edges[0][0] and location[0] + size[0]/2 <= self.edges[1][0]:
            return location[0] + size[0]/2 - self.edges[0][0]
        if location[0] - size[0]/2 <= self.edges[1][0] and location[0] - size[0]/2 >= self.edges[0][0]:
            return self.edges[1][0] - (location[0] - size[0]/2)
        if location[0] + size[0]/2 >= self.edges[0][0] and location[0] - size[0]/2 <= self.edges[1][0]:
            return self.size[0]
        if location[0] + size[0]/2 <= self.edges[1][0] and location[0] - size[0]/2 >= self.edges[0][0]:
            return size[0]
        return 0"""
        return (location[0]+size[0]/2) - self.edges[0][0]

    # return the high of overlap of the post in the 'location' and 'size', and self.
    def getOverlapHigh(self,location,size):
        """if location[1] + size[1]/2 >= self.edges[0][1] and location[1] + size[1]/2 < self.edges[2][1]:
            return location[1] + size[1]/2 - self.edges[2][1]
        if location[1] - size[1]/2 <= self.edges[2][1] and location[1] - size[1]/2 > self.edges[1][1]:
            return self.edges[1][0] - (location[1] - size[1]/2)
        if location[1] + size[1]/2 >= self.edges[0][1] and location[1] - size[1]/2 <= self.edges[2][1]:
            return self.size[1]
        if location[1] + size[1]/2 < self.edges[2][1] and location[1] - size[1]/2 > self.edges[1][1]:
            return size[1]
        return 0"""
        return self.edges[3][1] - (location[1] - size[1]/2)

    # determine how the post will be printed
    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    pass

