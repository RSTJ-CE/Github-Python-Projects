from pw_strength_check import *
from password_suggestor import *

def main():
    password = input('Enter password: ')
    missing_reqs = missing_requirements(password,requirements())

    # loops infinitely until password is accepted
    while missing_reqs != 'pass':
        for req_matching, num, req_name, str_name in missing_reqs:
            print(f'Password is missing {num} {str_name}')
        suggested_pw = suggest_password(password,missing_reqs)
        print(f'\nsuggested password: {suggested_pw}')
        acceptance = input(f'Accept password? (y/n)').lower()
        if acceptance == 'y':
            password = suggested_pw
            missing_reqs = missing_requirements(password,requirements())
        else:
            password = input('\nEnter password: ')
            missing_reqs = missing_requirements(password, requirements())

    print(f'\n{password} is your new password')

if __name__ == '__main__':
    main()