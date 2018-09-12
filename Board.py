
from Post import *
import pygame

def waitToClose():
    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT or checkForkey("q"):  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
    pygame.display.quit()

class Board:

    def __init__(self, w, h, id, region):
        self.posts = []  # contain posts object
        self.width = int(w)      # the width of the board
        self.high = int(h)      # the high of the board
        self.id = str(id)
        self.region = region  # the region of the board
        self.Board = None       # the surface of the board itself
        self.children = []      # sub boards od this board

    # function to call before showing the board
    def init(self):
        pygame.init()
        self.board = pygame.display.set_mode([self.width, self.high])
        self.board.fill(WHITE)
        pygame.display.set_caption(self.id+" "+self.region)

    # draw the posts that in the list on an initialize board (init()).
    def draw(self, color=BLACK):
        self.board.fill(WHITE)
        for p in self.posts:
            pygame.draw.aalines(self.board, p.color, True, p.edges)  # darw the lines of the posts
            font = pygame.font.SysFont('arial', 16)         # draw the name of the post
            name = font.render(p.name, True, p.color)
            self.board.blit(name, [p.location[0] - (len(p.name) * 2), p.location[1] - 5])
        pygame.display.update()

    def close(self):
        self.board.quit()

    def addPostByDetail(self, name, location, size):
        self.addPost(Post(name, location, size))

    def addPost(self, post):
        self.posts.append(post)

    def addPosts(self, posts):  # 'posts' is a list of posts
        for p in posts:
            self.addPost(p)

    def removePost(self, post):
        if post in self.posts:
            self.posts.remove(post)
        for board in self.children:  # remove the post if found in a child board
            if post in board.posts:
                board.posts.remove(post)

    def clear(self):
        self.posts.clear()
        for board in self.children:
            board.posts.clear()

    # check if the post in the board
    def isPostIn(self, location, size):
        if (location[0] - size[0] / 2) < 0 \
                or (location[1] - size[1] / 2) < 0 \
                or (location[0] + size[0] / 2) > self.width \
                or (location[1] + size[1] / 2) > self.high:
            return False
        return True

    # return if can add the post to the board
    def canAdd(self, x, y, size):
        for post in self.posts:
            if post.isPostIn([x, y], size):
                return False
        return self.isPostIn([x, y], size)

    # check if the mouse location in legal place then add the post and draw the board
    def checkPress(self, name, x, y, size):
        if self.canAdd(x, y, size):
            p = Post(name, [x, y], size)
            self.addPost(p)
            self.draw()
            return True
        else:
            return False

    # return if the mouse location is in the board
    def isMouseInWindow(self, x, y):
        if x < 0 or y < 0 or x > self.width or y > self.high:
            return False
        return True

    # let the user add post ('name', 'size') manualy.
    def UserAddPost(self, name, size):
        done = False
        shown = False
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT or checkForkey("q"):  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
            if not shown:
                x, y = pygame.mouse.get_pos()
                if self.isMouseInWindow(x, y):
                    if any(pygame.mouse.get_pressed()): # if the mouse was pressed
                        if self.checkPress(name, x, y, size): # check where and add the post
                            shown = True  # the post been posted
                        wait(0.1)  # so the click on the mouse will stop
                    if self.canAdd(x, y, size):    # if can add the post where the mouse is, draw the post in black
                        p = Post(name, [x, y], size)
                        self.addPost(p)
                    else:                           # if can't add the post where the mouse is, draw the post in red
                        p = Post(name, [x, y], size, color=RED)
                        self.addPost(p)
                    self.draw()        # draw the post and then remove it  just to show to user when he can add the post
                    self.removePost(p)
        pygame.display.quit()   # if the user press on exit so quit
        if shown:       # if the post, posted return
            return
        for child in self.children: # if not try to add it in the sub boards
            child.init()
            child.UserAddPost(name,size)

    # shot the board and his poats
    def show(self):
        #pdb.set_trace()
        done = False
        self.init()
        while not done:
            self.draw()
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT or checkForkey("q"):  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
        pygame.display.quit()
        for child in self.children:
            child.show()

    # return the post by name if found in self.posts
    def findPost(self, name):
        for post in self.posts:
            if post.name == name:
                return post
        return None


    def isPostExist(self,name):
        for p in self.posts:
            if p.name == name:
                #printMessege("post name: \"" + name + "\" already exist in board number: " + self.id)
                return True
        return False


    # add post automaticly to the default place: starting from right top and left
    def addPostAuto(self, name, size):
        # say the post is in this board
        if self.isPostExist(name):
            return self.id
        location = [0, 0]
        space = 2  #space between the posts and the edges of the board
        maxHighToAdd = 0  # when moving to next line, go down to the max high so the new line will be straight
        location[1] = size[1] / 2 + space
        while location[1] + (size[1]) / 2 < self.high - space:
            location[0] = self.width - (size[0]) / 2 - space
            location[1] += maxHighToAdd + space
            maxHighToAdd = 0
            while location[0] - size[0] / 2 > space and location[1] + (size[1]) / 2 < self.high - space:
                widthToSub = 0
                for p in self.posts:
                    if p.isPostIn(location, size):
                        widthToSub += p.getOverlapWidth(location, size)  # subtract the overlap in width of the two posts
                        if maxHighToAdd < p.getOverlapHigh(location, size):  # find the max overlap in high of the two posts
                            maxHighToAdd = p.getOverlapHigh(location, size)
                location[0] -= widthToSub + space
                if widthToSub == 0 and self.isPostIn(location, size):
                    self.addPostByDetail(name, location, size)
                    return self.id
        for child in self.children:
            if child.addPostAuto(name,size):
                return child.id
        return None

    def __str__(self):
        return str(self.__dict__)

if __name__ == "__main__":
    """b = Board(210,510,1)
    b.init()
    p1 = Post("1",[500,500],[200,200])
    p2 = Post("1",[100,200],[100,200])
    #pdb.set_trace()
    i = 2
    b.addPostAuto(1,[100,150])
    b.addPostAuto(2,[100,200])
    b.addPostAuto(3,[100,200])
    b.addPostAuto(4,[100,200])
    b.draw()
    wait(0.5)
    waitToClose()
    b.addPosts([p1,p2])
    b.draw()
    b.UserAddPost("חברי הטובים באמת",[150,150])
    pygame.quit()
    quit()"""





