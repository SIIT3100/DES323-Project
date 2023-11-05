from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.models import File,User 
import requests 

# Create your views here.
def database_item_list_by_id (request, fuid):
    dataset_objs = File.objects.filter(fUID__UID=fuid)
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(id),
        "datasets":dataset_objs
    }
    return render(request, 'WebApp/view.html' , context= context_data)

def database_item_delete(request, id):
    dataset_objs = File.objects.filter(fID=id)
    if len(dataset_objs) <= 0:
        return HttpResponse("ID Not found")
    Uid = dataset_objs.first().fUID.UID
    dataset_objs.delete()

    dataset_objs = File.objects.filter(fUID__UID=Uid)
    context_data = {
        "filter_type":str(id),
        "datasets":dataset_objs
    }
    #dataset_objs.delete()
    return render(request, 'WebApp/view.html' , context= context_data)

'''def database_item_edit(request, id):
    try:
        item = File.objects.get(fID=id)
    except:
        return HttpResponse("ID Not found")
    context_data = {
        'item_id': id,
        'form_data':{
            'file': item.file
            }
    }

    

    url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/sentiment_analyze/"

    querystring = {"text":"great value in its price range!"}

    headers = {
        "X-RapidAPI-Key": "88584e470amsh820791e23792648p1e6451jsne53bd64fe92d",
        "X-RapidAPI-Host": "twinword-twinword-bundle-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    return render(request, 'WebApp/editfile.html', context= context_data)'''

from django.shortcuts import render, HttpResponse, redirect
import json
import requests
from .models import File

def database_item_edit(request, id):
    try:
        item = File.objects.get(fID=id)
    except File.DoesNotExist:
        return HttpResponse("ID Not found")

    # Extract the content of the 'file' FieldFile as a string
    try:
        file_content = item.file.read().decode('utf-8')  # Assuming it's a text file
    except AttributeError:
        return HttpResponse("File content not found")

    json_data = json.loads(file_content)

    # Print the JSON data for debugging
    print(json_data)

    url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/sentiment_analyze/"

    headers = {
        "X-RapidAPI-Key": "88584e470amsh820791e23792648p1e6451jsne53bd64fe92d",
        "X-RapidAPI-Host": "twinword-twinword-bundle-v1.p.rapidapi.com"
    }

    responses = []
    combined_data=[]

    for sentence_data in json_data:
        sentence = sentence_data.get("message", "")
        querystring = {"text": sentence}
        response = requests.get(url, headers=headers, params=querystring)
        responses.append(response.json())

        #print(response.json())

        # Combine message and response into a dictionary
        combined_entry = {
            "message": sentence,
            "sentiment_response": response.json()
        }

        combined_data.append(combined_entry)

    #print(responses)
    print(combined_data)


    context_data = {
        'item_id': id,
        'form_data': {
            'file': json_data
        }
    }

    return render(request, 'WebApp/editfile.html', context= context_data)
