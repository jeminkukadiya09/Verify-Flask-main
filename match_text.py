# import Levenshtein as lev
from fuzzywuzzy import fuzz


# function to match any general string
def match_name(text, name):
    name_ratio = fuzz.partial_ratio(name.lower(), text.lower())
    return name_ratio


# function to match aadhar number
def match_aadhar_no(text, id_no):
    id_match = ""
    count = 0
    for i in id_no:
        if i.isnumeric():
            id_match += i
            count += 1
            if count % 4 == 0 and count != 12:
                id_match += " "
        elif i == ' ':
            continue
        else:
            return 0
    # print("ID MATCH = ", id_match)
    if count == 12:
        id_ratio = fuzz.partial_ratio(id_match, text)
        return id_ratio
    else:
        return 0


# function to match DL number
def match_dl_no(text, id_no):
    # print(text)
    # id_match = ''
    count = 0
    # print('id =', id_no)

    # pre-processing
    for i in id_no:
        if (count < 2 and i.isalpha()) or (count < 15 and i.isnumeric()):
            # id_match += i
            count += 1
        elif i == ' ' or i == '-':
            continue
        else:
            return 0
    # print('id_match =', id_match)
    id_ratio = fuzz.partial_ratio(id_no, text)
    return id_ratio


# match passport id
def match_passport_id(text, id_no):
    id_ratio = fuzz.partial_ratio(id_no, text)
    return id_ratio


# function to pre-process DOB and match it according to the separator
def match_dob(text, dob, sep):
    temp = ''
    count = 0
    date = ['', '', '']
    dob += '/'
    for i in dob:
        # print(i)
        if i.isnumeric():
            temp += i
        elif i == '.' or i == '-' or i == '/':
            if count < 3:
                date[count] = temp
                temp = ''
                count += 1
            else:
                return 0
        else:
            return 0
    date_match = date[0] + sep + date[1] + sep + date[2]
    date_ratio = fuzz.partial_ratio(date_match, text)
    # print(date_ratio)
    return date_ratio
