from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from database.models import File
from database.models import User as Users
import requests 
import json
import requests
import io

from openai import OpenAI

import os

import random

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
from django.contrib import messages
from .models import User


def generate_summary(sentences):
    # print(sentences)
    # from openai import OpenAI
    client = OpenAI(
    api_key='',  # this is also the default, it can be omitted
    )
    selected_sentences = random.sample(sentences, min(15, len(sentences)))
    prompt = "In a neutral tone, tell in one short sentence why the reviews are good and bad for the following sentences:\n"
    prompt += "\n".join(f"{i + 1}. {sentence}" for i, sentence in enumerate(selected_sentences))
    completion = client.completions.create(
        model='text-babbage-001',
        prompt = prompt,
        max_tokens= 100
        )
    print(completion.choices[0].text)
    #print(dict(completion).get('usage'))
    #print(completion.model_dump_json(indent=2))
    return completion.choices[0].text

def list(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('application/register')  # Redirect to the signup page if username exists

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('application/register')  # Redirect to the signup page if email exists

            new_user = User(username=username, email=email, password=password)
            new_user.save()

            messages.success(request, 'You are registered and can now log in')
            return redirect('application/login')  # Redirect to the login page
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('application/register')  # Redirect to the signup page

    return render(request, 'WebApp/list_view.html')

# Create your views here.
def database_login(request):
    if request.method=="POST":
        Username=request.POST["username"]
        Password=request.POST["password"]
        dataset_objs = Users.objects.filter(username=Username)
        if not Username or not Password:
            return render(request, 'WebApp/login.html', {'error_message': 'Both username and password are required'})
        if len(dataset_objs) <= 0:
            return render(request, 'WebApp/login.html', {'error_message': 'User not found'})
        #HttpResponse("User Not found" )
        dataset_objs = Users.objects.filter(username=Username,password = Password)
        if len(dataset_objs) <= 0:
            return render(request, 'WebApp/login.html', {'error_message': 'Wrong password!'})
        #HttpResponse("Wrong Password!" )
        
        print("Help")
        print(dataset_objs.first().UID)
        return redirect('database_item_upload', uid=dataset_objs.first().UID)

def database_create_new_user(request):
    if request.method=="POST":
        Email =request.POST["email"]
        Username=request.POST["username"]
        Password=request.POST["password"]
        Confirm_pass = request.POST["confirm_password"]
        if not Email or not Username or not Password or not Confirm_pass:
            return render(request, 'WebApp/reg.html', {'error_message': 'All fields are required'})
        dataset_objs = Users.objects.filter(email = Email)  
        dataset_objs = Users.objects.filter(username=Username)
        if len(dataset_objs) > 0:
            return render(request, 'WebApp/reg.html', {'error_message': 'Username already registered'})
            #HttpResponse("Already have this username" )
            
        if len(dataset_objs) > 0:
            return render(request, 'WebApp/reg.html', {'error_message': 'Email already registered'})
            #HttpResponse("Already have this Email" )
            
        if Confirm_pass != Password:
            return render(request, 'WebApp/reg.html', {'error_message': 'Password does not match'})
        
        New_User  = Users.objects.create(
                                        username=Username,
                                        email=Email,
                                        password=Password,
                                        pfp="www.a.com",
                                        )

        dataset_objs = Users.objects.filter(username=Username)
        print("Help")
        print(dataset_objs.first().UID)
        return redirect('core_views_login')

def database_item_upload (request, uid):
    #dataset_objs = File.objects.filter(fUID__UID=uid)
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(uid),
        "uid":str(uid),
    }
    return render(request, 'WebApp/upload.html' , context= context_data)


import csv
import json

def database_render_aboutus(request, uid):
    context_data = {
        "filter_type":str(uid),
        "uid":str(uid),
    }
    return render(request, 'WebApp/aboutL.html' , context= context_data)

def database_item_add(request, uid):
    if request.method=="POST":
        if 'Files' in request.FILES:
            csv_file = request.FILES['Files']

            # Read CSV data
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

            # Assuming the first row of the CSV file contains headers
            headers = next(csv_data)

            # Convert CSV data to a list of dictionaries
            csv_list = [dict(zip(headers, row)) for row in csv_data]

            # Remove BOM from keys
            csv_list = [{key.strip("\ufeff"): value for key, value in item.items()} for item in csv_list]

            # Convert the list of dictionaries to a JSON string
            json_data = json.dumps(csv_list)

            # Create a ContentFile from the JSON data
            content_file = ContentFile(json_data.encode('utf-8'))

            print(json_data)

            Uid, created = Users.objects.get_or_create(UID=uid)
            item = File.objects.create(
                                        fName=csv_file.name,
                                        file=content_file,
                                        fDateTime=datetime.now(),
                                        fUID=Uid,
                                        )
            # Add the ContentFile to the File object
            item.file.save("new_file.json", content_file)

            json_data = json.loads(item.file.read().decode('utf-8'))

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
                sentence = sentence_data.get("message", sentence_data.get("Text", ""))
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
                
            #overall_summary = generate_summary([sentence_data.get("message", sentence_data.get("Text", "")) for sentence_data in json_data])
            #print("Overall Summary:", overall_summary)

            #print(responses)
            print(combined_data)
            
            # Serialize the combined data as a JSON string
            combined_json = json.dumps(combined_data)

            # Create a ContentFile from the serialized JSON data
            combined_json_file = ContentFile(combined_json.encode('utf-8'))

            # Update the 'file' field of the item with the new content
            item.file.save("new_file.json", combined_json_file)
            fid = item.fID

            return redirect('database_homeShowTest' , fid=fid, uid=uid)
    
    
    return redirect('database_item_upload', uid=uid)

def database_statistic (request, fid, uid):
    try:
        item = File.objects.get(fID=fid)
    except File.DoesNotExist:
        return HttpResponse("ID Not found")

    # Extract the content of the 'file' FieldFile as a string
    try:
        file_content = item.file.read().decode('utf-8')  # Assuming it's a text file
    except AttributeError:
        return HttpResponse("File content not found")
    
    json_data = json.loads(file_content)
    name = item.fName
    
    overall_summary = generate_summary([sentence_data.get("message", sentence_data.get("Text", "")) for sentence_data in json_data])
    print("Overall Summary:", overall_summary)
    
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(fid),
        "uid":str(uid),
        "name":name,
        "datasets":json_data,
        "overall_summary": overall_summary
    }
    return render(request, 'WebApp/homeShowTest.html' , context= context_data)
            

def database_item_list_by_id (request, fuid):
    dataset_objs = File.objects.filter(fUID__UID=fuid)
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(id),
        "uid":str(fuid),
        "datasets":dataset_objs
    }
    return render(request, 'WebApp/view.html' , context= context_data)

def database_item_delete(request, fid):
    dataset_objs = File.objects.filter(fID=fid)
    if len(dataset_objs) <= 0:
        return HttpResponse("ID Not found")
    Uid = dataset_objs.first().fUID.UID
    dataset_objs.delete()

    dataset_objs = File.objects.filter(fUID__UID=Uid)
    context_data = {
        "filter_type":str(fid),
        "uid":str(Uid),
        "datasets":dataset_objs
    }
    #dataset_objs.delete()
    return render(request, 'WebApp/view.html' , context= context_data)


def database_item_edit(request, fid):
    try:
        item = File.objects.get(fID=fid)
    except File.DoesNotExist:
        return HttpResponse("ID Not found")

    # Extract the content of the 'file' FieldFile as a string
    try:
        file_content = item.file.read().decode('utf-8')  # Assuming it's a text file
    except AttributeError:
        return HttpResponse("File content not found")
    
    json_data = json.loads(file_content)
    Uid = item.fUID.UID
    #if len(dataset_objs) <= 0:
        #return HttpResponse("ID Not found" )
    context_data = {
        "filter_type":str(fid),
        "uid":str(Uid),
        "datasets":json_data,
        "fName": item.fName,
        "fDateTime": item.fDateTime,
        "fSize": item.file.size/1000,
    }
    return render(request, 'WebApp/editfile.html' , context= context_data)

def user_profile(request, uid):
    item = User.objects.filter(UID = uid)
    context = {
        "uid":str(uid),
        "datasets":item
    }
    return render(request, "WebApp/profile.html", context=context) 

def update_name(request, fid):
    if request.method == 'POST':
        new_fName = request.POST.get('new_fName')
        # fID = request.POST.get('fID')
        
        try:
            # Use get() instead of filter() to get a single instance
            item = File.objects.get(fID=fid)
        except File.DoesNotExist:
            return HttpResponse("ID Not found")
        
        # Update the attributes and save the model instance
        item.fName = new_fName
        item.fDateTime = datetime.now()
        item.save()

        Uid = item.fUID.UID

        return redirect('database_item_list_by_id', fuid=Uid)

    # Handle other cases or render a response if needed
    return HttpResponse("Invalid request")
        
        

def update_user(request, uid):
    if request.method == 'POST':
        new_Username = request.POST.get('new_Username')
        new_Email = request.POST.get('new_Email')
        #print(uid)
        # fID = request.POST.get('fID')
        
        try:
            # Use get() instead of filter() to get a single instance
            item = User.objects.get(UID=uid)
        except File.DoesNotExist:
            return HttpResponse("ID Not found")
        
        # Update the attributes and save the model instance
        item.username = new_Username
        item.email = new_Email
        item.save()


        return redirect('user_profile', uid=uid)

    # Handle other cases or render a response if needed
    return HttpResponse("Invalid request")


    

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