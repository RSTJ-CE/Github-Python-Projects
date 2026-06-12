import re
import string
#Strong password consists of at least 8 length, 1 symbol, 1 uppercase, 1 lowercase and 1 number

def requirements(num=1,upper=1,lower=1,special_char=1):
    #defines requirements for strong password
    special_characters = string.punctuation
    digits = string.digits
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    reqs = [
        (num, r'\d',digits, 'number'), #0-9
        (upper, r'[A-Z]',uppercase, 'uppercase character'), #A-Z
        (lower, r'[a-z]',lowercase, 'lowercase character'), #a-z
        (special_char, fr'[{special_characters}]',special_characters, 'special character') #special characters on keyboard
        ]
    #each elements returns req_matching,number,req_name,string_name
    return reqs

def missing_requirements(password,reqs,min_length=8):
    missing_reqs = []
    all_characters = string.ascii_letters + string.digits + string.punctuation

    if len(password) < min_length: #if password length is < minimum length
        missing_reqs.append(['',min_length - len(password),all_characters, 'more length'])
        #adds req_matching,number,req_name,string_name to the list
    for number_of_req,req_match,req_name,str_name in reqs: #loops over requirements
        length_of_matched_requirements = len(re.findall(req_match,password))
        #len(re.findall(req_match,password)) returns number of matches of password to specific requirements
        if number_of_req > length_of_matched_requirements: #checks if every requirement are met
            number_of_missing_req = number_of_req - length_of_matched_requirements
            missing_reqs.append([req_match,number_of_missing_req,req_name,str_name])
    if missing_reqs: #if there is a requirement not fulfilled
        return missing_reqs
    else: #if password passes
        return 'pass'


if __name__ == '__main__': #check if returned list is valid
    password = input('Password: ')
    print(missing_requirements(password,requirements()))




