import requests
from bs4 import BeautifulSoup
import datetime
from requests_html import HTMLSession
from tqdm import tqdm
from pprint import pprint
import pandas as pd
import openpyxl


def get_file():
    page = 1
    web_dict = {'Заголовок статьи': [], 'Ссылка на статью': [], 'Страница на Хабр': [], 'Номер статьи': [],
                'Дата публикации': [], 'Время публикации': [], 'Актуальность статьи в днях': [], 'Статья без заголовка': [],
                }
    while page <= 50:
        session = HTMLSession()
        url = f'https://habr.com/ru/all/page{page}/'
        response = session.get(url=url).text
        base_url = 'https://habr.com'
        KEYWORDS = ['дизайн', 'фото', 'web', 'python']

        soup = BeautifulSoup(response, features='html.parser')
        articles = soup.find(class_='tm-articles-list').find_all('article')
        for id, article in tqdm(enumerate(articles)):
            if article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2'):
                web_head = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').text
                web_href = base_url + article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').contents[0].attrs['href']
                time_publication = article.find(class_='tm-article-snippet__datetime-published').contents[0].attrs['title']
                data_p = datetime.date(int(time_publication[0:4]), int(time_publication[5:7]), int(time_publication[8:10]))
                time_p = datetime.time(int(time_publication[12:14]), int(time_publication[15:17])).strftime("%X")
                date_dif = (datetime.date.today() - data_p).days
                pub_data = data_p.strftime("%d %B %Y")
                tags = article.find(class_='tm-article-snippet__hubs')
                for tag in tags:
                    tag_name = tag.text.strip().lower().split()[0]
                    if tag_name in KEYWORDS:
                        web_dict['Заголовок статьи'] += [web_head]
                        web_dict['Ссылка на статью'] += [web_href]
                        web_dict['Дата публикации'] += [pub_data]
                        web_dict['Время публикации'] += [time_p]
                        web_dict['Актуальность статьи в днях'] += [date_dif]
                        web_dict['Страница на Хабр'] += [page]
                        web_dict['Номер статьи'] += [id + 1]
                        web_dict['Статья без заголовка'] += ["---"]
            elif article.find(class_='tm-megapost-snippet__title'):
                web_not_title = article.find(class_='tm-megapost-snippet__title').text
                datetime_no_head = article.find(class_='tm-megapost-snippet__link tm-megapost-snippet__date').contents[0].attrs['title']
                date_no_head = datetime.date(int(datetime_no_head[0:4]), int(datetime_no_head[5:7]), int(datetime_no_head[8:10])).strftime("%d %B %Y")
                time_no_head = datetime.time(int(datetime_no_head[12:14]), int(datetime_no_head[15:17])).strftime("%X")
                href_no_head = base_url + article.find(class_='tm-megapost-snippet__link tm-megapost-snippet__date').attrs['href']
                dif_date = (datetime.date.today() - datetime.date(int(datetime_no_head[0:4]), int(datetime_no_head[5:7]), int(datetime_no_head[8:10]))).days
                web_dict['Заголовок статьи'] += ["---"]
                web_dict['Ссылка на статью'] += [href_no_head]
                web_dict['Дата публикации'] += [date_no_head]
                web_dict['Время публикации'] += [time_no_head]
                web_dict['Актуальность статьи в днях'] += [dif_date]
                web_dict['Страница на Хабр'] += [page]
                web_dict['Номер статьи'] += [id + 1]
                web_dict['Статья без заголовка'] += [web_not_title]
            else:
                techno_web = article.find(class_='tm-voice-article__body').contents[0].contents[0].contents[1].attrs['href']
                title_rek = article.find(class_='tm-voice-article__body').text
                web_dict['Заголовок статьи'] += ["---"]
                web_dict['Ссылка на статью'] += [techno_web]
                web_dict['Дата публикации'] += ["---"]
                web_dict['Время публикации'] += ["---"]
                web_dict['Актуальность статьи в днях'] += ["---"]
                web_dict['Страница на Хабр'] += [page]
                web_dict['Номер статьи'] += [id + 1]
                web_dict['Статья без заголовка'] += [title_rek]
        page += 1
    return web_dict

if __name__ == '__main__':
    df = pd.DataFrame(get_file())
    df.to_excel("Habr_scraping.xlsx")


