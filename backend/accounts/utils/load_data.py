import csv
from accounts.models import CustomUser, Follow
import chardet
import requests
import random
import math
import ast

from decimal import Decimal

def fix_data(csv_path):
    with open(csv_path, 'rb') as csvfile:
        content = csvfile.read()
        content = content.decode('ascii', 'replace')
        content = content.encode('ascii', 'replace')


    with open(csv_path, 'wb') as csvfile:
        csvfile.write(content)

def load_data_from_csv(csv_path):
    user_details = requests.get('https://randomuser.me/api/?results=5000')
    user_details = user_details.json()["results"]
    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for row in reader:
            # create an instance of MyModel for each row in the CSV file
            user = random.choice(user_details)
            # [["id", "following_list", "clean_input", "languages", "job", "bio", "lat", "lon"]]
            lat = row[6]
            lon = row[7]

            if not lat.isnumeric():
                lat = None
            
            if not lon.isnumeric():
                lon = None

            obj = CustomUser(id=row[0], first_name=user["name"]["first"], last_name=user["name"]["last"],
                             email=f"generated_user_{count}@ai.com", bio=row[5], job=row[4], lat=lat, lon=lon, location=row[8], profile_photo=user["picture"]["large"])
            data.append(obj)
            print(f"Added: {row[0]}")
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

def update_follows(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for row in reader:
            user = CustomUser.objects.get(id=row[0])
            find = Follow.objects.filter(follower=user)
            if len(find) == 0:
                likes = ast.literal_eval(row[1])[0:100]
                liked_users = CustomUser.objects.filter(pk__in=likes)
                for i in liked_users:
                    Follow.objects.create(follower=user, following=i)
                print(f"Added: {row[0]}")
    