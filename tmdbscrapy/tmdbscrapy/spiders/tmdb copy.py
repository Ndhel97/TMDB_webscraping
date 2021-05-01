import scrapy


class TmdbSpider(scrapy.Spider):
    name = 'tmdb'
    allowed_domains = ['www.themoviedb.org']
    start_urls = ['https://www.themoviedb.org/movie?page=1']

    def parse(self, response):
        # for movie in response.css('div.page_wrapper'):
        for i in range(1, 21):
            movie = response.xpath('/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div['+ str(i) +']/div[2]')
            movie_details = response.urljoin(movie.css('a::attr(href)').get())
            yield{
                'link': movie.css('a::attr(href)').get(),
                'title': movie.css('a::attr(title)').get(),
                'score': movie.css('div::attr(data-percent)').get()
            }
            # scrapy.Request(movie_details, callback=self.parse_details)
            
        next_page = response.xpath('/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[24]/p/a')
        next_page = next_page.css('a.no_click::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
    # def parse_details(self, response):
    #     # new_response = scrapy.Request(movie_details)
    #     details = response.xpath('/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div')
    #     yield{
    #         'release': details.css('span::text').get()
    #     }
            
