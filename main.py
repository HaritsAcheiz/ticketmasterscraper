from urllib.parse import urljoin

from httpx import Client
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import pandas as pd

@dataclass
class TicketScraper:
    base_url:str = 'https://www.ticketmaster.com'


    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        headers2 = {
            'Host': 'www.ticketmaster.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.ticketmaster.com/search',
            'x-tmlangcode': 'en-us',
            'x-tmplatform': 'global',
            'x-tmregion': '200',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        client = Client(headers=headers2)
        # client.get(self.base_url)
        response = client.get(url)
        if response.status_code != 200:
            print('Failed')
            response.raise_for_status()
        print(response)

        return response.json()

    def get_data(self, json_data):
        item_summaries = json_data['events']
        items_exist = False
        for item in item_summaries:
            if items_exist:
                temp_data = pd.DataFrame.from_dict(item, orient='index')
                temp_data = temp_data.transpose()
                items = pd.concat([items, temp_data], copy=True)
            else:
                items = pd.DataFrame.from_dict(item, orient='index')
                items = items.transpose()
                items_exist = True
        items.to_csv('sample_data_San_Fransisco_event.csv', index=False)


    def main(self):
        endpoint = '/api/search/events?q=&region=200&page=0&distance=6214&distanceUnit=miles&latitude=37.778&longitude=-122.4313'
        url = urljoin(self.base_url, endpoint)
        json_data = self.fetch(url)
        print(json_data)
        self.get_data(json_data)

        return

if __name__ == '__main__':
    s = TicketScraper()
    s.main()