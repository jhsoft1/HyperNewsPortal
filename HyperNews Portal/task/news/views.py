import itertools
import json
import os
import random

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.datetime_safe import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON_PATH = os.path.join(os.path.dirname(BASE_DIR), 'task/hypernews/news.json')
with open(NEWS_JSON_PATH, 'r') as json_file:
    # with open(settings.NEWS_JSON_PATH, "r") as json_file:
    news = json.load(json_file)
links = set([new['link'] for new in news])
free_links = list(set(range(10000)) - links)


def index_view(request):
    query = request.GET.get('q')
    if query != '' and query is not None:
        filtered_news = [new for new in news if query in new['title']]
        print(filtered_news)
    else:
        filtered_news = news
    sorted_news = sorted(filtered_news, key=lambda i: i['created'], reverse=True)
    grouped_news = [{'date': date, 'values': list(news)} for date, news in
                    itertools.groupby(sorted_news, lambda i: i['created'][:10])]
    context = {"grouped_news": grouped_news}
    return render(request, "news/index.html", context=context)


def create_view(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, "news/index2.html")
    else:
        text = request.POST.get('text')
        title = request.POST.get('title')
        new_link = random.choice(free_links)
        free_links.remove(new_link)
        news.append({'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'text': text, 'title': title, 'link': new_link})
        with open(NEWS_JSON_PATH, 'w') as json_file:
            json.dump(news, json_file)
        return redirect('/')


def link_view(request, link):
    new = next((i for i in news if i["link"] == link), None)
    context = {"new": new}
    return render(request, "news/index1.html", context=context)
