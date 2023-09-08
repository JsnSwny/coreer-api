import csv
from accounts.models import CustomUser, Follow, Project
import chardet
import requests
import random
import math
import ast
import json


from decimal import Decimal

def fix_data(csv_path):
    with open(csv_path, 'rb') as csvfile:
        content = csvfile.read()
        content = content.decode('ascii', 'replace')
        content = content.encode('ascii', 'replace')


    with open(csv_path, 'wb') as csvfile:
        csvfile.write(content)

def load_data_from_csv(csv_path):
    csv.field_size_limit(1000000)
    user_details = requests.get('https://randomuser.me/api/?results=5000')
    user_details = user_details.json()["results"]
    count = 0
    with open(csv_path, mode='r', encoding='utf-16') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for idx, row in enumerate(reader):
            # create an instance of MyModel for each row in the CSV file
            user = random.choice(user_details)
            # [["id", "following_list", "clean_input", "languages", "job", "bio", "lat", "lon"]]
            # lat = row[6]
            # lon = row[7]

            # if not lat.isnumeric():
            #     lat = None
            
            # if not lon.isnumeric():
            #     lon = None

            obj = CustomUser(id=row[0], first_name=user["name"]["first"], last_name=user["name"]["last"],
                             email=f"user_{count}@coreer.co", bio=row[3], job=row[10], profile_photo=user["picture"]["large"])
            data.append(obj)
            print(f"Added: {idx}")
            count += 1

    # # use Django's ORM to bulk insert the objects into the database
    CustomUser.objects.bulk_create(data)


def update_data(csv_path):
    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for row in reader:
            # [["id", "following_list", "clean_input", "languages", "job", "bio", "lat", "lon"]]
            user = CustomUser.objects.get(id=row[0])

            try:
                user.lat = Decimal(row[6])
                user.lon = Decimal(row[7])
            except:
                print("Didn't work")

            user.save()
            print(f"Added: {row[0]}")

def update_bios():
    csv.field_size_limit(1000000)
    with open("accounts/data/data-16.csv", mode='r', encoding='utf-16') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for idx, row in enumerate(reader):
            user = CustomUser.objects.get(id=row[0])
            user.bio = row[3]
            user.tfidf_input = row[9]
            user.save()
            print(f"Added: {idx}")

def update_projects():
    csv.field_size_limit(1000000)
    with open('accounts/data/projects.json', 'r') as f:
        data = json.load(f)
        for idx, i in enumerate(data):
            user = CustomUser.objects.get(id=i["id"])
            for project in i['repo_list']:
                obj = Project(user=user, title=project['full_name'], start_date=project['created_at'][:10], description=project['description'])
                obj.save()

            print(f"Added: {idx}")
            
        

def update_locations():
    csv.field_size_limit(1000000)
    with open("accounts/data/data-16.csv", mode='r', encoding='utf-16') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for idx, row in enumerate(reader):
            user = CustomUser.objects.get(id=row[0])
            print(row[11], row[12], row[13])
            if(row[13]):
                user.lat = Decimal(row[11])
                user.lon = Decimal(row[12])
                user.location = row[13]
            else:
                user.lat = None
                user.lon = None
                user.location = None
                print("Is Nan")
            user.save()
            print(f"Added: {idx}")

def update_follows(csv_path):
    csv.field_size_limit(1000000)
    with open(csv_path, mode='r', encoding='utf-16') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for idx, row in enumerate(reader):
            user = CustomUser.objects.get(id=row[0])
            find = Follow.objects.filter(follower=user)
            if len(find) == 0:
                likes = ast.literal_eval(row[5])[0:100]
                liked_users = CustomUser.objects.filter(pk__in=likes)
                for i in liked_users:
                    Follow.objects.create(follower=user, following=i)
                print(f"Added: {idx}")

def update_languages(csv_path):
    csv.field_size_limit(1000000)
    with open(csv_path, mode='r', encoding='utf-16') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for idx, row in enumerate(reader):
            user = CustomUser.objects.get(id=row[0])
            if not user.languages.all().exists():
                languages = ast.literal_eval(row[7])[0:100]
                for i in languages:
                    user.add_language(i)
                print(f"Added: {idx}")

def update_types():
    users = CustomUser.objects.all()
    for user in users:
        user.type = CustomUser.PROFESSIONAL
        if user.job:
            if user.job.lower() == "student":
                user.type = CustomUser.STUDENT             
        user.save()