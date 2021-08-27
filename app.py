import scrapy

class FlipkartScrap(scrapy.Spider):
    name = "flipkart"
    
    start_urls = ['https://www.flipkart.com/search?q={prod}'.format(prod = "google phone")]

    def parse(self, response):

        names = response.xpath("//div[@class='_4rR01T']/text()").getall()
        prices = response.xpath("//div[@class='_30jeq3 _1_WHN1']/text()").getall()
        imgs = response.xpath("//img[@class='_396cs4 _3exPp9']/@src").getall()
        flipkart = []
        for i in range(len(names)):
            d2 = {}
            d2['shopping_site']="flipkart"
            d2['product_name']=names[i]
            d2['product_price']=prices[i].replace("\u20b9", "")
            d2['product_image'] = imgs[i]
            flipkart.append(d2)


        yield {"flipkart": flipkart}
        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)

