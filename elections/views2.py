from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

import json
# Create your views here.
def index(request):
    candidates = Candidate.objects.all()

    with open('./elections/test.json', 'rt', encoding='utf-8-sig') as json_file:
        json_data = json.load(json_file)

    #for i in range(len(json_data)):
    for i in range(5):
        new_candidate = Candidate(name=json_data[i]["day"], introduction=json_data[i]["title"],area=json_data[i]["count"],party_number=json_data[i]["link"])
        new_candidate.save()

    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)
