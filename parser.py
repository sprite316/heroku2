import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import json

from elections.models import Candidate
Candidate.objects.all().delete()

def toJson(mnet_dict):
    with open('title_link.json', 'w', encoding='utf-8') as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')

def parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1,8):
        url = 'https://www.ygosu.com/community/real_article?page={}'.format(page)
        html = urlopen(url)
        source = html.read()
        html.close()

        soup = BS(source, "html.parser")
        table = soup.find(class_="board_wrap")
        tits = table.find_all(class_="tit")
        counts = table.find_all(class_="read")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = tit.a.get('href')
            read = count.get_text()
            date = day.get_text()
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
            temp_list.append(temp_dict)

    #toJson(temp_list)

    return temp_list

#parsing()

if __name__=='__main__':
    parsed_data = parsing()
    for i in range(len(parsed_data)):
        new_candidate = Candidate(name=parsed_data[i]["day"],
        introduction=parsed_data[i]["title"],
        area=parsed_data[i]["count"],
        party_number=parsed_data[i]["link"])
        new_candidate.save()
