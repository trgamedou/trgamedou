import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

start_date = datetime.strptime("12-11-23", "%m-%d-%y")

today = datetime.today()
today -= timedelta(days=2)

file_name = f'news-({start_date.strftime("%#m-%#d-%y")})-({today.strftime("%#m-%#d-%y")}).csv'

header = [
    'date', 'time', 'page link',
    'title 1', 'description 1', 'image 1', 'source 1',
    'title 2', 'description 2', 'image 2', 'source 2',
    'title 3', 'description 3', 'image 3', 'source 3',
    'title 4', 'description 4', 'image 4', 'source 4',
    'title 5', 'description 5', 'image 5', 'source 5',
    'title 6', 'description 6', 'image 6', 'source 6',
    'title 7', 'description 7', 'image 7', 'source 7',
    'title 8', 'description 8', 'image 8', 'source 8',
    'title 9', 'description 9', 'image 9', 'source 9',
    'title 10', 'description 10', 'image 10', 'source 10',
]

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)

current_date = start_date
while current_date <= today:
    formatted_date = current_date.strftime("%#m-%#d-%y")
    # print(formatted_date) -> 12-11-23
    news_times = ['10am', '3pm', '8pm']
    for news_time in news_times:
        if formatted_date == '12-11-23' and (news_time == '10am' or news_time == '3pm'):
            continue
        response = requests.get(f'https://www.yews.news/edition/{formatted_date}-{news_time}')
        soup = BeautifulSoup(response.content.decode('utf-8'))
        page_data = {
            'news_1' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_2' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_3' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_4' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_5' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_6' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_7' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_8' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_9' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            },
            'news_10' : {
                'title' : None,
                'image' : None,
                'description' : None,
                'source' : None
            }
        }
        titles = soup.find_all('div', {'class' : 'whole-body'})

        count = 0
        for title in titles:
            count+=1
            page_data[f'news_{count}']['title'] = title.text

        descriptions = soup.find_all('div', {'class' : 'expand'})

        count = 0
        for description in descriptions:
            count+=1
            image_element = description.find('img', src=lambda x: x and x != '')
            if image_element:
                image_link = image_element.get('src')
            else:
                image_link = None
            page_data[f'news_{count}']['image'] = image_link

            final_description = final_description = description.get_text(separator=' ', strip=True).replace('This is some text inside of a div block. Source', '')

            page_data[f'news_{count}']['description'] = final_description
            source_link = description.find('div', {'class' : 'location'}).find('a').get('href')
            page_data[f'news_{count}']['source'] = source_link
        
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            data = [
                formatted_date, news_time, f'https://www.yews.news/edition/{formatted_date}-{news_time}',
                page_data['news_1']['title'], page_data['news_1']['description'], page_data['news_1']['image'], page_data['news_1']['source'],
                page_data['news_2']['title'], page_data['news_2']['description'], page_data['news_2']['image'], page_data['news_2']['source'],
                page_data['news_3']['title'], page_data['news_3']['description'], page_data['news_3']['image'], page_data['news_3']['source'],
                page_data['news_4']['title'], page_data['news_4']['description'], page_data['news_4']['image'], page_data['news_4']['source'],
                page_data['news_5']['title'], page_data['news_5']['description'], page_data['news_5']['image'], page_data['news_5']['source'],
                page_data['news_6']['title'], page_data['news_6']['description'], page_data['news_6']['image'], page_data['news_6']['source'],
                page_data['news_7']['title'], page_data['news_7']['description'], page_data['news_7']['image'], page_data['news_7']['source'],
                page_data['news_8']['title'], page_data['news_8']['description'], page_data['news_8']['image'], page_data['news_8']['source'],
                page_data['news_9']['title'], page_data['news_9']['description'], page_data['news_9']['image'], page_data['news_9']['source'],
                page_data['news_10']['title'], page_data['news_10']['description'], page_data['news_10']['image'], page_data['news_10']['source'],
            ]
            writer.writerow(data)

    current_date += timedelta(days=1)
