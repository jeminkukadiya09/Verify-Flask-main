import cv2
import os
import pandas as pd


def is_present(image_path, yml_type="training"):
    yml_path = os.path.join(os.curdir, "ymls", yml_type + ".yml")

    # df = pd.read_csv('uid.csv')
    # function to check if face already exists in data
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(yml_path)
    except:
        return False
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # # indicate id counter
    # id = 0
    # names = ['none'] + df['UID'].to_list()

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    minW = "64"
    minH = "48"
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    if (len(faces) == 0):
        print("NO FACE DETECTED")
        return True
    print("CHECKING FOR FACES")
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        # If confidence is less them 100 ==> "0" : perfect match
        if confidence < 50:
            # cv2.putText(
            #     img,
            #     "ERROR",
            #     (x + 5, y - 5),
            #     font,
            #     1,
            #     (0, 0, 255),
            #     2
            # )
            # cv2.putText(
            #     img,
            #     "Press any key to EXIT",
            #     (x + 5, y + h - 5),
            #     font,
            #     1,
            #     (255, 255, 0),
            #     1
            # )
            # cv2.imshow('camera', img)
            # cv2.waitKey(0)
            # cam.release()
            # cv2.destroyAllWindows()
            return True
        else:
            return False


def recog():
    # df = pd.read_csv('uid.csv')
    # function to recognize face and return corresponding UID
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read('trainer/trainer.yml')
    except:
        print("No trained data")
        return
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # indicate id counter
    id = 0
    names = ['none'] + df['UID'].to_list()
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # If confidence is less them 100 ==> "0" : perfect match
            if confidence < 100:
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(
                img,
                str(id),
                (x + 5, y - 5),
                font,
                1,
                (255, 255, 255),
                2
            )
            cv2.putText(
                img,
                str(confidence),
                (x + 5, y + h - 5),
                font,
                1,
                (255, 255, 0),
                1
            )

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
    # cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recog()
