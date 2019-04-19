import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
import argparse


def createParser():
    parser = argparse.ArgumentParser(description='Проверка ссылки')
    parser.add_argument('link')

    return parser


def shorten_link(long_url, token):
    url_bit_shorten = "https://api-ssl.bitly.com/v3/shorten"
    data = {"access_token": token,
            "longUrl": long_url}
    response = requests.post(url_bit_shorten, data=data)
    return response.json()['data']['url']


def check_link_clicks_summary(url, token):
    url_get_summary = "https://api-ssl.bitly.com/v3/link/clicks"
    data = {"access_token": token,
            "link": url,
            "units": -1}
    response = requests.get(url_get_summary, params=data)
    response.raise_for_status()
    if not response.ok:
        return None
    try:
        return response.json()['data']['link_clicks']
    except TypeError:
        return None


def main(link):
    if not requests.get(link).ok:
        print("Wrong link")
        return

    load_dotenv(join(dirname(__file__), '.env'))
    token = os.environ.get("TOKEN")

    link_clicks = check_link_clicks_summary(link, token)
    if link_clicks is not None:
        print("Количество переходов по ссылке:", link_clicks)
        return

    print(shorten_link(link, token))


if __name__ == '__main__':

    parser = createParser()
    args = parser.parse_args()
    main(args.link)
