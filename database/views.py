from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from database.models import File
from database.models import User as Users
import requests 
import json
import requests
from django.core.files.base import ContentFile

from django.contrib.auth.models import User
from database.serializers import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.urls import reverse


# Create your views here.
def database_login(request):
    if request.method=="POST":
        Username=request.POST["username"]
        Password=request.POST["password"]
        dataset_objs = Users.objects.filter(username=Username)
        if len(dataset_objs) <= 0:
            return HttpResponse("User Not found" )
        dataset_objs = Users.objects.filter(username=Username,password = Password)
        if len(dataset_objs) <= 0:
            return HttpResponse("Wrong Password!" )
        
        print("Help")
        print(dataset_objs.first().UID)
        return redirect('database_item_upload', uid=dataset_objs.first().UID)

def database_create_new_user(request):
    if request.method=="POST":
        Email =request.POST["email"]
        Username=request.POST["username"]
        Password=request.POST["password"]
        dataset_objs = Users.objects.filter(email = Email)
        if len(dataset_objs) > 0:
            return HttpResponse("Already have this Email" )
        
        dataset_objs = Users.objects.filter(username=Username)
        if len(dataset_objs) > 0:
            return HttpResponse("Already have this username" )
        
        New_User  = Users.objects.create(
                                        username=Username,
                                        email=Email,
                                        password=Password,
                                        pfp="www.a.com",
                                        )

        dataset_objs = Users.objects.filter(username=Username)
        print("Help")
        print(dataset_objs.first().UID)
        return redirect('database_item_upload', uid=dataset_objs.first().UID)

def database_item_upload (request, uid):
    #dataset_objs = File.objects.filter(fUID__UID=uid)
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(uid)
    }
    return render(request, 'WebApp/upload.html' , context= context_data)



def database_item_add(request, uid):
    if request.method=="POST":
        #print("help")
        csv = request.FILES["Files"]

        Uid, created = Users.objects.get_or_create(UID=uid)
        audio_file = File.objects.create(
                                    fName=csv.name,
                                    file=csv,
                                    fDateTime=datetime.now(),
                                    fUID=Uid,
                                      )
        audio_path= audio_file.file.path
        return redirect('database_item_upload', uid=uid)
    
    
    return redirect('database_item_upload', uid=uid)
            

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
    
    # Serialize the combined data as a JSON string
    combined_json = json.dumps(combined_data)

    # Create a ContentFile from the serialized JSON data
    combined_json_file = ContentFile(combined_json.encode('utf-8'))

    # Update the 'file' field of the item with the new content
    item.file.save("new_file.json", combined_json_file)

    context_data = {
        'item_id': id,
        'form_data': {
            'file': json_data
        }
    }

    return render(request, 'WebApp/editfile.html', context= context_data)


#api
@csrf_exempt
def api_item_delete(request, id):
    if request.method == "DELETE":
        
        dataset_objs = File.objects.filter(fID=id)
        if len(dataset_objs) <= 0:
            return JsonResponse({"status":"Failed","message":"Not Found"}, status=400)
        Uid = dataset_objs.first().fUID.UID
        dataset_objs.delete()

        dataset_objs = File.objects.filter(fUID__UID=Uid)
        context_data = {
            "filter_type":str(id),
            "datasets":dataset_objs
        }
        #dataset_objs.delete()
        return JsonResponse({"status":"Success","message":"Row Deleted"}, status=200)
    return JsonResponse({"status":"Failed","message":"False Method"}, status=400)


@csrf_exempt
def api_item_process(request, id):
    if request.method == "POST":
        try:
            item = File.objects.get(fID=id)
        except File.DoesNotExist:
            return JsonResponse({"status":"Failed","message":"Not Found"}, status=400)

        # Extract the content of the 'file' FieldFile as a string
        try:
            file_content = item.file.read().decode('utf-8')  # Assuming it's a text file
        except AttributeError:
            return JsonResponse({"status":"Failed","message":"Incorrect Format"}, status=400)

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
        
        # Serialize the combined data as a JSON string
        combined_json = json.dumps(combined_data)

        # Create a ContentFile from the serialized JSON data
        combined_json_file = ContentFile(combined_json.encode('utf-8'))

        # Update the 'file' field of the item with the new content
        item.file.save("new_file.json", combined_json_file)

        context_data = {
            'item_id': id,
            'form_data': {
                'file': json_data
            }
        }

        return JsonResponse({"status":"Success","message":"File Processed"}, status=200)
    return JsonResponse({"status":"Failed","message":"False Method"}, status=400)
      