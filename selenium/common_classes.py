class Article:
   
    def __init__(self, url, title, numComments):
        self.url = url
        self.title = title
        self.numComments = numComments
        self.topComment = ''
        self.age = 0
        self.topCommentNum = 0
        self.tag = ''
        self.img = ''

    def __init__(self, url):
        self.url = url
        self.title = ''
        self.numComments = 0
        self.topComment = ''
        self.age = 0
        self.topCommentNum = 0
        self.tag = ''
        self.img = ''

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
    @property
    def img(self):
        return self.img

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
    def numComments(self, value):
        self.numComments = value
    @img.setter
    def img(self, value):
        self.img = value        

class CSSXPATH:

   def __init__(self, path, attribute, pathType):
    if pathType.lower() in "css":
        pathType = "css"
    elif pathType.lower() in "xpath":
        pathType = "xpath"
    else:
        raise ValueError ("CSSXPATH class error: must be css or xpath")

    #if pathType.lower() != "css" or pathType.lower() != "xpath":
    #    raise ValueError ("CSSXPATH class error: must be css or xpath")
    if len(path) == 0:
        raise ValueError ("CSSXPATH class error: path is 0")
    self.pathType = pathType
    self.path = path
    self.attribute = attribute

    @property
    def pathType(self):
        return self.pathType
    @property
    def path(self):
        return self.path
    @property
    def attribute(self):
        return self.attribute
