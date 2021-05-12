import match_text


def match(img_text, form_data):
    # name_ratio = 0
    # dob_ratio = 0
    # gender_ratio = 0
    # id_ratio = 0
    # address_ratio = 0
    print(form_data)

    name_ratio = match_text.match_name(img_text, form_data["name"])
    dob_ratio = match_text.match_dob(img_text, form_data["dob"], '/')
    print("NAME AND DOB RATIO", name_ratio, dob_ratio)
    gender = form_data["gender"]
    gender_ratio = 0
    # valid = 0
    if gender == 'Male':
        gender_ratio = match_text.match_name(img_text, "MALE")
        if match_text.match_name(img_text, "FEMALE") == 100:
            gender_ratio = 0
        # valid = 1
    elif gender == 'Female':
        gender_ratio = match_text.match_name(img_text, "FEMALE")
        # valid = 1
    else:
        gender_ratio = match_text.match_name(img_text, "TRANSGENDER")

    print("Gender checked")
    id_ratio = match_text.match_aadhar_no(img_text, form_data["docid"])
    # address_ratio = match_text.match_name(img_text, form_data["address"])

    print("ID Checked")

    address_ratio = 0
    address = form_data["address"].split()
    # print(address)
    img_text = img_text.lower()

    for word in address:
        if word.lower() in img_text:
            address_ratio += 1
    address_ratio = address_ratio/float(len(address)) * 100

    print(address, address_ratio)
    print(form_data["dob"], dob_ratio)
    print([name_ratio, dob_ratio, gender_ratio, id_ratio, address_ratio])
    print("Everything checked")
    if name_ratio < 90 or dob_ratio < 100 or gender_ratio < 100 or id_ratio < 100 or address_ratio < 80.0:  #EDIT 90->80
        return False
    else:
        return True
