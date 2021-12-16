from dataAnalyzer.models import Item
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import bs4, requests
def get_data(page, no_page: int):
        link_item = page.find_all('a', {'class': 'card-v2-title semibold mrg-btm-xxs js-product-url'}, href=True)
        price_item = page.find_all('p', {'class': 'product-new-price'})
        links = [link['href'] for link in link_item]
        texts = [link.get_text() for link in link_item]
        prices=[]
        for price in price_item:
            if price.get_text()!='':
                prices.append(float(price.get_text().split(" Lei")[0][:2]+'.'+price.get_text().split(" Lei")[0][2:]))
        data = []
        for i in range(len(links)):
            data.append([links[i], texts[i], prices[i]])
        return data
def init_scraper(url):
        print('requesting page...')
        print(url)
        ### create a request
        page = requests.get(url)
        ### parse table with bs4
        page_soup = bs4.BeautifulSoup(page.text, 'html.parser')
    

        return page_soup
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def __init__(self):
        self.url_to_scrap = 'https://www.emag.ro/'
        self.URL_INIT = 'https://www.emag.ro/cereale/c?ref=search_menu_category'
        
    def add_arguments(self, parser):
        parser.add_argument('--category', '-c', type=str, default="")

    def handle(self, *args, **options):
        if(options['category']!=''):
            #session = DatabaseHandler.session
            #page = init_scraper(URL_INIT)
            category = options['category']
            url_for_scrap = self.url_to_scrap + category
            page = requests.get(url_for_scrap)
            if(page.status_code == 404):
                raise ValueError("The category doesnt exist")
            ### parse table with bs4
            page_soup = bs4.BeautifulSoup(page.text, 'html.parser')
            initial_next_page = page_soup.find_all('a', {'aria-label': 'Next'})[0]
            page_nr = 1
            datas = []
            datas.append(get_data(page_soup, page_nr))
            while(initial_next_page.get_text() != 'Pagina anterioara'):
                datas.append(get_data(page_soup, page_nr))
                page_nr += 1
                next_link = self.url_to_scrap[:-1] + initial_next_page['href']
                next_page = init_scraper(next_link)
                initial_next_page = next_page.find_all('a', {'aria-label': 'Next'})[-1]
            for index in datas:
                for data in index:
                    i = Item(name = data[1], item_type = category, current_date = datetime.now(), current_price = data[2], link = data[0]).save()
        else:
            raise ValueError("Must specify a category")
    
