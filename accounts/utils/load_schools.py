import csv
from accounts.models import CustomUser, Follow, School
import chardet
import requests
import random
import math
import ast
import json
from bs4 import BeautifulSoup
import certifi
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import base64
from urllib.parse import urljoin
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import re



def load_schools(json_file):
    count = 0
    with open(json_file, encoding='utf-8') as f:
        print(f)
        data = json.load(f)
        for i in data:
            obj = School(name=i["name"], country=i["country"])
            obj.save()
            count += 1

def load_images(json_file, n):
    disable_warnings(InsecureRequestWarning)
    with open(json_file, encoding='utf-8') as f:
        print(f)
        data = json.load(f)

        schools = School.objects.filter(logo=None, id__gte=n)

        for school in schools:
            school_data = data[school.id -1]
            url = school_data["web_pages"][0]
            print(f"{school.id} - {school.name}")
            try:

            
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                response = requests.get(url, verify=False, headers=headers, timeout=8)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                apple_touch_icon = soup.find('link', rel='apple-touch-icon')

                favicon_url = None

                if apple_touch_icon:
                    favicon_url = urljoin(url, apple_touch_icon["href"])
                else:
                    match = re.search('<link rel="icon" type="image/.*?" href="(.*?)">', response.text)
                    if match:
                        favicon_url = match.group(1)
                    else:
                        print("No match")

                if favicon_url:
                    # download the favicon image
                    favicon_response = requests.get(favicon_url, headers=headers)
                    favicon_response.raise_for_status()

                    favicon_bytes = favicon_response.content
                    favicon_io = io.BytesIO(favicon_bytes)
                    favicon_file = InMemoryUploadedFile(favicon_io, None, f"{school_data['name'].replace(' ', '-').lower()}-favicon.png", 'image/x-icon', len(favicon_bytes), None)
                    school.logo = favicon_file
                    school.save()
                    print(f"{school_data['name']} Saved")
            except requests.exceptions.RequestException as e:
                print("Error connecting to {}: {}".format(url, e))

            
            # with open('icon.png', 'wb') as f:
            #     f.write(icon_response.content)

import boto3
from django.core.files.base import ContentFile

def fix_images():
    s3 = boto3.client('s3')
    bucket_name = 'coreer-static'

    for obj in School.objects.all():
        s3_key = f"media/logos/{obj.name.replace(' ', '-').lower()}-favicon.png"
        try:
            response = s3.get_object(Bucket=bucket_name, Key=s3_key)
            image_data = response['Body'].read()

            obj.logo.save(s3_key, ContentFile(image_data), save=True)
            print(f"Found Key - {s3_key}")
        except:
            print(f"No key - {s3_key}")