import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdbscrapymovies'
    allowed_domains = ['www.themoviedb.org']
    start_urls = ['https://www.themoviedb.org/movie?page=1']

    def parse(self, response):
        for i in range(1, 21):
            movie = response.xpath('/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div['+ str(i) +']/div[2]')
            movie_details = response.urljoin(movie.css('a::attr(href)').get())
            yield scrapy.Request(movie_details, callback=self.parse_details)
            
        next_page = response.xpath('/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[24]/p/a')
        next_page = next_page.css('a.no_click::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_details(self, response):
        details = response.xpath('/html/body/div[1]/main/section/div[2]')
        clean_image_urls = []
        clean_image_urls.append('https://www.themoviedb.org' + ''.join(details.xpath('//*[@id="original_header"]/div[1]/div/div[1]/img/@src').get(default='null').split('_filter(blur)')))
        yield{
            'title': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()').get(),
            'link': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/@href').get(),
            'release': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]/text()').get().split()[0:2],
            'genre': {
                'genre1': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a[1]/text()').get(),
                'genre2': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a[2]/text()').get(),
                'genre3': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a[3]/text()').get(),
                'genre4': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a[4]/text()').get(),
                'genre5': details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a[5]/text()').get()
                },
            'runtime': ''.join(details.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]/text()').get(default='null').split()),
            'score': details.xpath('//*[@id="original_header"]/div[2]/section/ul/li[1]/div[1]/div/div/@data-percent').get(),
            'overview': details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/div/p/text()').get(),
            'poster': ''.join(details.xpath('//*[@id="original_header"]/div[1]/div/div[1]/img/@src').get(default='null').split('_filter(blur)')),
            'people': {
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[1]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[1]/p[1]/a/text()').get(),
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[2]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[2]/p[1]/a/text()').get(),
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[3]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[3]/p[1]/a/text()').get(),
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[4]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[4]/p[1]/a/text()').get(),
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[5]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[5]/p[1]/a/text()').get(),
                details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[6]/p[2]/text()').get(): details.xpath('//*[@id="original_header"]/div[2]/section/div[2]/ol/li[6]/p[1]/a/text()').get(),
                },
            'image_urls': clean_image_urls
        }

    
            
