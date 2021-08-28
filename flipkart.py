import scrapy

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com']

    def __init__(self, category='', **kwargs):
        self.start_urls = [f"https://www.flipkart.com/search?q={category}"]  # py36
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        names = response.xpath("//div[@class='_4rR01T']/text()").getall()
        prices = response.xpath("//div[@class='_30jeq3 _1_WHN1']/text()").getall()
        imgs = response.xpath("//img[@class='_396cs4 _3exPp9']/@src").getall()
        for i in range(len(names)):
            yield {
                "shopping_site":"flipkart", 
                "product_name":names[i], 
                "product_price":prices[i].replace("\u20b9", ""), 
                "product_image":imgs[i]
            }

        names = response.xpath("//a[@class='s1Q9rs']/text()").getall()
        prices = response.xpath("//div[@class='_30jeq3']/text()").getall()
        imgs = response.xpath("//img[@class='_396cs4 _3exPp9']/@src").getall()
        print(names)
        print(imgs)
        print(prices)
        
        for i in range(len(names)):
            yield {
                "shopping_site":"flipkart", 
                "product_name":names[i], 
                "product_price":prices[i].replace("\u20b9", ""), 
                "product_image":imgs[i]
            }
