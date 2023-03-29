import csv
from accounts.models import CustomUser, Follow, School
import chardet
import requests
import random
import math
import ast
import json

def load_schools():
    count = 0
    with open("accounts/data/universities.json", 'r') as f:
        print(f)
        # data = json.load(f)
        # bulk_data = []
        # for i in data:
        #     obj = School(name=i["name"], country=i["country"])
        #     bulk_data.append(obj)
        #     count += 1

    # # use Django's ORM to bulk insert the objects into the database
    # School.objects.bulk_create(data)