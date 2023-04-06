import requests
from bs4 import BeautifulSoup
import string
import os


pages = int(input("Please enter the number of pages you wish to scrape"))
article_type = input("Please enter the article tag you wish to search for, for example 'News'")

url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="

for page in range(1, pages + 1):
    r = requests.get(url + str(page), headers={'Accept-Language': 'en-US,en;q=0.5'})

    # fetch the articles with the sub-category 'news'
    if r.status_code == 200:
        # build folder & change working directory
        os.mkdir(f"Page_{page}")
        os.chdir(f"Page_{page}")

        # scrape website
        soup = BeautifulSoup(r.content, 'html.parser')

        news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=article_type)

        news_article_dict = {}
        for news_article in news_article_links:
            anchor = str(news_article.find_parent('article').find('a', {'data-track-action': 'view article'}))
            anchor = anchor.split('"')

            # sanitise article title for use as a filename
            anchor[12] = anchor[12].replace("</a>", "")

            for digit in anchor[12]:
                if digit in string.punctuation:
                    anchor[12] = anchor[12].replace(digit, "")

            anchor[12] = anchor[12].replace(" ", "_")

            news_article_dict[anchor[12]] = anchor[9]

        # determine the root of the url
        url_root = url.split(".com")
        url_root = f"{url_root[0]}.com"

        # fetch body each article
        for article in news_article_dict:
            article_r = requests.get(url_root + news_article_dict[article], headers={'Accept-Language': 'en-US,en;q=0.5'})
            article_soup = BeautifulSoup(article_r.content, 'html.parser')

            article_body = article_soup.find('p', class_='article__teaser').text.strip()

            # save article in its own file
            with open(f"{article}.txt", "w") as file:
                class_attribute = '{"class": "article__teaser"}'
                file.write(article_body)

        # change working directory to one step up
        os.chdir('..')

    else:
        print("Invalid page!")
