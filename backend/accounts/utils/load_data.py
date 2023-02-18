import csv
from accounts.models import CustomUser
import chardet
import requests


def fix_data(csv_path):
    with open(csv_path, 'rb') as csvfile:
        content = csvfile.read()
        content = content.decode('ascii', 'replace')
        content = content.encode('ascii', 'replace')


    with open(csv_path, 'wb') as csvfile:
        csvfile.write(content)

def load_data_from_csv(csv_path):

    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = []
        for row in reader:
            # create an instance of MyModel for each row in the CSV file
            obj = CustomUser(first_name="Jason", last_name="Sweeney", email=f"generated_user_{count}@ai.com", bio=row[1])
            data.append(obj)
            print(f"Added: {row[0]}")
            count += 1
    # # use Django's ORM to bulk insert the objects into the database
    CustomUser.objects.bulk_create(data)