from scrapy.item import Item, Field

class DmozItem(Item):
    title = Field()
    link = Field()
    pop = Field()
    comment = Field()
    pub = Field()
    typeContent = Field()
    age = Field()



