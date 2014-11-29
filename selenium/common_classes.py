class Article:
   
    def __init__(self, url, title, numComments):
        self.url = url
        self.title = title
        self.numComments = numComments
        self.topComment = ''
        self.age = 0
        self.topCommentNum = 0
        self.tag = ''

    def __init__(self, url):
        self.url = url
        self.title = ''
        self.numComments = 0
        self.topComment = ''
        self.age = 0
        self.topCommentNum = 0
        self.tag = ''

    @property   
    def url(self):
        return self.url
    @property    
    def title(self):
        return self.title
    @property    
    def numComments(self):
        return self.numComments
    @property            
    def topComment(self):
        return self.topComment
    @property    
    def topCommentNum(self):
        return self.topCommentNum
    @property
    def age(self):
        return self.age
    @property
    def tag(self):
        return self.tag        

    @topComment.setter    
    def topComment(self, value):
        self.topComment = value
    @topCommentNum.setter
    def topCommentNum(self, value):
        self.topCommentNum = value
    @age.setter        
    def age(self, value):
        self.age = value
    @tag.setter
    def tag(self, value):
        self.tag = value
    @title.setter
    def title(self, value):
        self.title = value
    @numComments.setter
    def title(self, value):
        self.title = value

