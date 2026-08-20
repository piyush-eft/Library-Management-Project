import json
from pathlib import Path
import string
import random
from datetime import datetime


class Library:

    database = "library.json"
    data = {"books": [], "members":[]}

    # LOAD EXISTING DATA TO JSON FILE OR CREATE YOUR JSON
    if Path(database).exists():
        with open(database,"r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    else:
        with open(database,'w') as f:
            json.dump(data,f,indent=4)


    def gen_id(Prefix ="B"):
        random_id =""
        for i in range(5):
            random_id += random.choice(string.ascii_uppercase + string.digits)

        return Prefix + "-" + random_id




    def add_book(self):
        title = input("What is the title of the book :-")
        author = input("Who is the author of the book :=")
        copies = int(input("How many copies do you have :-"))

        book = {

            "Id" : Library.gen_id(),
            "Title" : title,
            "Author" : author,
            "Total_copies" : copies,
            "Available_copies" : copies,
            "Add_on" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }

        Library.data['books'].append(book)








hello =Library()



print("="*50)
print("Library Management System")
print("="*50)
print("1. Add Book")
print("2. List Book")
print("3. Add Member")
print("4. List Member")
print("5. Borrow Book")
print("6. Return Book")
print("0. Exit Portal")
print("-"*50)

choice = int(input("Please tell which task you want to perform"))

if choice ==1:
    hello.add_book()