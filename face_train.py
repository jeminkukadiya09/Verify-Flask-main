import cv2
import numpy as np
from PIL import Image
import os

# , yml_path='trainer/trainer.yml'

def train(training_path,yml_type="training"):
    yml_path = os.path.join(os.curdir,"ymls",yml_type+".yml")
    # path = new_path
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    print("Starting to train")
    print("training_path =",training_path)
    print("yml_path =",yml_path)
    # function to get the images and label data
    def getImagesAndLabels(path):
        idPaths = [os.path.join(path, f) for f in os.listdir(path)]
        idList = [idx for idx in os.listdir(path)]
        faceSamples = []
        ids = []
        print("idPaths =",idPaths)
        print("idList =",idList)
        # for idPath in idPaths:
        for i in range(0,len(idPaths)):
            captures_path_images = os.path.join(idPaths[i], "captures")
            imagePaths = [os.path.join(captures_path_images,f) for f in os.listdir(captures_path_images)]
            print("imagePaths =",imagePaths)
            for imagePath in imagePaths:
                # imagePath = os.path.join(training_path)
                PIL_img = Image.open(imagePath).convert('L')  # grayscale
                img_numpy = np.array(PIL_img, 'uint8')
                # EDIT id = imagePath #get uuid from folder
                # id = int(id[-4:])
                idx = i
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(idx)

        return faceSamples, ids

    # OK!~
    # SORRY!~
    faces, ids = getImagesAndLabels(training_path)
    print("ids =",ids)
    print("Length of ids =",len(ids))
    print("Length of faces =",len(faces))


    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    # recognizer.write('trainer/trainer.yml')
    recognizer.write(yml_path)
