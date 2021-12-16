import requests
import bs4
from dataAnalyzer.models import Item
from datetime import datetime


class Scrapper():
    def __init__(self):
        self.url_to_scrap = 'https://www.emag.ro/'
        self.URL_INIT = 'https://www.emag.ro/cereale/c?ref=search_menu_category'

    def init_scraper(self, url):
        print('requesting page...')
        print(url)
        # create a request
        page = requests.get(url)
        # parse table with bs4
        page_soup = bs4.BeautifulSoup(page.text, 'html.parser')

        return page_soup

    def get_data(self, page, no_page):
        link_item = page.find_all(
            'a', {'class': 'card-v2-title semibold mrg-btm-xxs js-product-url'}, href=True)
        price_item = page.find_all('p', {'class': 'product-new-price'})
        links = [link['href'] for link in link_item]
        texts = [link.get_text() for link in link_item]
        prices = []
        for price in price_item:
            if price.get_text() != '':
                p = price.get_text().split(" Lei")[0]
                prices.append(
                    float(p[:len(p)-2].replace('.', '') + '.'+p[len(p)-2:]))
        data = []
        for i in range(len(links)):
            data.append([links[i], texts[i], prices[i]])
        return data
    # return zip(links, prices, texts)

    def run(self, category):
        #session = DatabaseHandler.session
        #page = init_scraper(URL_INIT)
        url_for_scrap = self.url_to_scrap + category
        initial_page = self.init_scraper(url_for_scrap)
        try:
            initial_next_page = initial_page.find_all(
                'a', {'aria-label': 'Next'})[0]
            page = 1
            datas = []
            datas.append(self.get_data(initial_page, page))
            while(initial_next_page.get_text() != 'Pagina anterioara'):
                datas.append(self.get_data(initial_page, page))
                page += 1
                next_link = self.url_to_scrap[:-1] + initial_next_page['href']
                next_page = self.init_scraper(next_link)
                initial_next_page = next_page.find_all(
                    'a', {'aria-label': 'Next'})[-1]
            for index in datas:
                for data in index:
                    i = Item(name=data[1], item_type=category, current_date=datetime.now(
                    ), current_price=data[2], link=data[0]).save()
        except:
            page = 1
            datas = []
            datas.append(self.get_data(initial_page, page))
            for index in datas:
                for data in index:
                    i = Item(name=data[1], item_type=category, current_date=datetime.now(
                    ), current_price=data[2], link=data[0]).save()
