from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_mail import Mail, Message

# from flask_pymongo import PyMongo
import pymongo


from PIL import Image
import pytesseract


import os
import base64
import uuid
import shutil

from datetime import datetime
import pytz


import aadhar_module

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtpout.secureserver.net',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'jeminkukadia@gmail.com',
	MAIL_PASSWORD = '123@#Varifie'
	)

mail = Mail(app)
CORS(app)

CURRENT_USERS_STORE = {}

# BUCKET_IN_USE = "1"
# UPLOAD_FOLDER = 'temp-'+BUCKET_IN_USE
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MONGO_URI"] = "mongodb+srv://dipanshujain895:96501@cluster0.3oh4q.mongodb.net/Varifie?retryWrites=true&w=majority"

# COLLECTION_IN_USE = "temp_users_"+BUCKET_IN_USE
# app.config["COLLECTION_IN_USE"] = COLLECTION_IN_USE

timezone = pytz.timezone("Asia/Kolkata")
datetime_IND = datetime.now(timezone)

print(datetime_IND.hour)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different


@app.route('/')
def hello_world():
    return 'Hello World!'

############################################
# View Routes

@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/cam')
def cam():
    return render_template("cam.html")

@app.route('/aadhar/<string:uid>')
def aadhar(uid):
    print(uid)
    return render_template("aadhar.html",data=uid,MATCH="")


@app.route('/passport')
def passport():
    return render_template("passport.html")


app.route('/voterid')
def voterid():
    return render_template('voterid.html')


@app.route('/license')
def license():
    return render_template('license.html')

############################################


# @app.route('/aadhar/<uuid:id>')
# def aadhar


@app.route('/check_image', methods=["POST"])
def check_image():
    if((datetime_IND.hour >= 0 and datetime_IND.hour < 6) or (datetime_IND.hour >= 12 and datetime_IND.hour < 18)):
        BUCKET_IN_USE = "1"
    else:
        BUCKET_IN_USE = "2"

    UPLOAD_FOLDER = 'temp-'+BUCKET_IN_USE
    if request.is_json:
        print("JSON Recieved")
        data = request.get_json()
        print(data,type(data))

        new_id = str(uuid.uuid1())
        all_images = data["frames"]
        curdir = os.getcwd()
        print(curdir)
        newdir = "/"+UPLOAD_FOLDER+"/" + new_id + '/captures'



        newpath = curdir + newdir
        print(newpath)

        # new_id = generate_new_id()
        try:
            os.makedirs(newpath)
        except OSError as error:
            print("Directory already there or", error)
        finally:
            count = 1
            for image in all_images:
                base64_img_bytes = image.encode('utf-8')

                # with open(os.path.join(newpath, 'frame-' + str(k) + ".png"), 'wb') as file_to_save:
                with open(os.path.join(newpath, new_id + '-' + str(count) + ".png"), 'wb') as file_to_save:
                    decoded_image_data = base64.decodebytes(base64_img_bytes)
                    file_to_save.write(decoded_image_data)
                count += 1

            image_path = os.path.join(newpath, "User." + str(new_id) + '.1' + ".png")
            # if not is_present(image_path):
            #     return jsonify({"found": False, "message": "New Uid Created for the face", "uid": new_id})
            # face_train.train(newpath)

        #     else:
        #         print("NO FACE FOUND, OR ALREADY PRESENT")
        #         return jsonify({"found": "true",
        #                         "error": "Either Face already present or no face found, Please try with a new face!!"}), 406
        #
        # return jsonify({"message": "kuch nhi chala"})

        print("Done!")

        CURRENT_USERS_STORE[new_id] = BUCKET_IN_USE
        return jsonify({"message": "Done!", "id": new_id})
    else:
        print("Something else received")
        return jsonify({"message": "kuch nhi chala"})



@app.route('/check_details', methods=["POST"])
def check_details():
    client = pymongo.MongoClient(app.config["MONGO_URI"])
    db = client["Varifie"]
    print("Recieved: ")
    print(request.form)

    # Uncomment this before performing real time calls just for the time being internet not available
    data = request.form
    idx = request.form["uuid"]
    BUCKET_IN_USE = CURRENT_USERS_STORE[idx]
    UPLOAD_FOLDER = 'temp-' + BUCKET_IN_USE
    COLLECTION_IN_USE = "temp_users_"+BUCKET_IN_USE
    temp_users = db[COLLECTION_IN_USE]

    #print(request.files)
    if(data["doctype"] == '/aadhar'):
        details = {

            "name": request.form["name"],
            "gender": request.form["gender"],
            "docid": request.form["idval"],
            "email": request.form["email"],
            "doctype": "aadhar",
            "address": request.form["address"],
            "dob": request.form["dob"],
            "uuid": request.form["uuid"]
        }



    if (request.files):
        img_text = ''

        print("I have some files for you!")
        print(request.files)
        print(len(request.files))
        images = request.files.getlist("files[]")
        print(images)
        count = 0
        new_id = data["uuid"]
        curdir = os.getcwd()
        print(curdir)
        newdir = "/" + UPLOAD_FOLDER + "/" + new_id + '/documents'
        newpath = curdir + newdir
        try:
            os.makedirs(newpath)
            print(newpath)
        except OSError as error:
            print("Directory already there or", error)
        finally:
            print(new_id)
            print(len(images))

            for i in range(0, len(images)):
                filename, fileextension = os.path.splitext(images[i].filename)
                print(filename, fileextension)
                image_path = os.path.join(newpath, new_id + "-" + str(count) + fileextension)
                images[i].save(image_path)
                img_text += pytesseract.image_to_string(Image.open(image_path))
                img_text += "\n"
                print('\n',img_text,'\n')

                print(images[i])
                count += 1
            res = aadhar_module.match(img_text, details)
            if res:
                print("Details matched")
                temp_users.insert_one(details)
                try:
                    msg = Message("Regarding Submission of Documents and Face ID",
                                  sender="info@varifie.com",
                                  recipients=[details["email"]])
                    msg.body = '''Hey {}, 
                    You have successfully submitted your documents with us along with your face captures.
                    Now we are Varifieing your documents and face capture and will update you with the status withing 6-8 hours.
                    
                    Thanks & Regards,
                    Varifie
                    '''.format(details["name"])
                    mail.send(msg)
                    # return 'Mail sent!'
                except Exception as e:
                    return (str(e))


            else:
                print("Didn't Match")
                shutil.rmtree(newpath)
                # return jsonify({"error": "NOT_MATCHED",
                #                 "message": 'Details not matched, please check your details and try again'}), 406
                return render_template("aadhar.html",data=idx)
            return render_template("confirm.html")
            #
            # for image in images:
            #     filename, fileextension = os.path.splitext(image.filename)
            #     print(filename, fileextension)
            #     image_path = os.path.join(newpath, new_id + str(count) + fileextension)
            #     print(image.save(image_path))
            #     print(image)


        # images['images'].save(os.path.join(app.config['UPLOAD_FOLDER'], images['images'].filename))

        # d = dict(request.files)
        # print(d)
    else:
        print("No Files Found")
        return jsonify({"error": "No files sent with the request!"}), 406


    del CURRENT_USERS_STORE[idx]
    # print("Recieved")
    return jsonify({"message": "details recieved"})

if __name__ == '__main__':
    app.run()
