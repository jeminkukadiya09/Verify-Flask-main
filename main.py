# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
import os
import base64
import shutil

import json
import pytesseract
from PIL import Image
# from generate_uid import generate_new_id
import face_recog
import face_train
import cv2
import pickle
import time
import requests
import pymongo
import pytz
from datetime import datetime
import schedule

config = { "MONGO_URI": "mongodb+srv://dipanshujain895:96501@cluster0.3oh4q.mongodb.net/Varifie?retryWrites=true&w=majority"}




def print_hi(name):

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



def work_on_dataset():
    timezone = pytz.timezone("Asia/Kolkata")
    datetime_IND = datetime.now(timezone)

    print(datetime_IND.hour)
    # EDIT Commented the if else for testing purposes
    if ((datetime_IND.hour >= 0 and datetime_IND.hour < 6) or (datetime_IND.hour >= 12 and datetime_IND.hour < 18)):
        BUCKET_IN_USE = "2"
    else:
        BUCKET_IN_USE = "1"


    # change_data(BUCKET_IN_USE)
    # BUCKET_IN_USE = "1"
    work_on_ids(BUCKET_IN_USE)

    # assign path according to bucket

    # for each uuid in bucket:
    #


def work_on_ids(BUCKET_TO_LOAD):

    path = os.path.join(os.curdir, "..","..","Varifie-Flask","temp-"+BUCKET_TO_LOAD)
    print(path)
    ids = os.listdir(path)
    if(len(ids)==0):
        return
    print("ids =",ids)
    training_path = os.path.join(os.curdir,"training")
    print("training_path =",training_path)

    for idx in ids:
        print("Current Id =",idx)
        process_data(idx,os.path.join(path,idx),BUCKET_TO_LOAD,training_path)
        print("Completed process for idx=",idx)

    training = os.listdir(training_path)
    print("training dataset obtained =",training)

    for idx in training:
        print("Current Id in training =",idx)
        captures_dir = os.path.join(training_path,idx, "captures")
        captures = os.listdir(captures_dir)

        capture = captures[0]

        image_path = os.path.join(captures_dir, capture)
        print("image_path =",image_path)
        if face_recog.is_present(image_path,"image_dump"):     # check for presence in main yml
            shutil.rmtree(path)
            removed = remove_data(idx)
            if (not removed):
                print("Error while deleting the record")

        #change_data(id,BUCKET_TO_LOAD)

    # shift everything in training to main dump

    # shift everything from temp_db to main db
    # retrain main dump
    users_path = os.path.join(os.curdir,"users")
    last_users = os.listdir(training_path)
    for user_x in last_users:
        shutil.move(os.path.join(training_path,user_x),users_path)

    main_users = os.listdir(users_path)
    for idx in main_users:
        change_data(idx,BUCKET_TO_LOAD)

    face_train.train(users_path,yml_type="image_dump")


def process_data(idx,path,BUCKET_TO_LOAD,training_path):

    # checking uniqueness in bucket
    captures_dir = os.path.join(path,"captures")
    captures = os.listdir(captures_dir)

    capture = captures[0]
    image_path = os.path.join(captures_dir,capture)
    print("image_path =",image_path)
    if(face_recog.is_present(image_path)):
        shutil.rmtree(path)
        removed = remove_data(idx,BUCKET_TO_LOAD)
        if(not removed):
            print("Error while deleting the record")
    else:
        # training_path = os.path.join(os.curdir,"training")
        # yml_path = os.path.join(training_path,"training.yml")
        shutil.move(path, os.path.join(training_path,idx))
        face_train.train(training_path,yml_type="training")
        print("New Face Detected")



    # check first image from idx... if face_recog.is_present():
        # remove idx folder from bucket
        # remove idx from temp_db
    # else:
        # shift to "training" folder
        # face_train.train()    # train everything in training folder
        # print"(new id generated")
    pass


def remove_data(idx,BUCKET_TO_LOAD):
    client = pymongo.MongoClient(config["MONGO_URI"])
    db = client["Varifie"]
    # UPLOAD_FOLDER = 'temp-' + BUCKET_TO_LOAD
    COLLECTION_IN_USE = "temp_users_" + BUCKET_TO_LOAD
    temp_users = db[COLLECTION_IN_USE]

    user = temp_users.find_one({"uuid": idx})
    print(user)
    if (user):
        # print(user)
        deleted = temp_users.delete_one({"uuid": user["uuid"]})
        if deleted:
            return True
        else:
            return False
    # temp_users.delete_one(user)

    pass

def change_data(idx, BUCKET_TO_LOAD):
    client = pymongo.MongoClient(config["MONGO_URI"])
    db = client["Varifie"]

    COLLECTION_IN_USE = "temp_users_" + BUCKET_TO_LOAD
    temp_users = db[COLLECTION_IN_USE]

    users = db["users"]
    user = temp_users.find_one({"uuid":idx})
    if(user):
        print(user)
        users.insert_one(user)
        temp_users.delete_one({"uuid": user["uuid"]})



    # temp_users.delete_one(user)

    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # work_on_ids("1")
    # work_on_dataset()
    while True:
        schedule.every().day.at("00:15").do(work_on_dataset)
        schedule.every().day.at("06:15").do(work_on_dataset)
        schedule.every().day.at("12:15").do(work_on_dataset)
        schedule.every().day.at("18:15").do(work_on_dataset)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
