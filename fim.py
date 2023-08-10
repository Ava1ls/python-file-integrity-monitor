import os
import sys
import time
import hashlib
from colorama import Fore, Back, Style, just_fix_windows_console
just_fix_windows_console()


HASH = hashlib.sha256()
baseline = ''


def hash_create(basepath, filename):
    with os.scandir(basepath) as entries:
        file_dictionary = []
        for entry in entries:
            if entry.is_file():  
                with open(entry, 'r') as file:
                    f_entry = file.read()
                    calculated_hash = hashlib.sha256(f_entry.encode('utf-8')).hexdigest()
                    entry_path = os.path.basename(entry) + ' | ' + calculated_hash
                    file_dictionary.append(entry_path)

    try:
        f_baseline = open(filename, 'x')

    except:
        f_baseline = open(filename, 'w')

    for file in file_dictionary:
        f_baseline.write('\n' + f'{file}')

    f_baseline.close()


def monitor(basepath, filename, tmp):
    try:
        while True:
            hash_create(basepath, 'hash_check.txt')
            
            file1 = open(filename,'r')
            file2 = open('hash_check.txt','r')

            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

            if len(file1_lines) == len(file2_lines):
                for i in range(len(file1_lines)):
                    if file1_lines[i] != file2_lines[i]:

                        tmp=file1_lines[i].split('|')

                        print(Fore.RED + 'ALERT: File ' + tmp[0] + ' was changed!')
                        print(Style.RESET_ALL)
            else:
                with open(filename, 'r') as file1:
                    with open('hash_check.txt', 'r') as file2:
                        diff = set(file1).difference(file2)

                diff.discard('\n')

                for x in diff:
                    output = x.strip(' | ')
                    print(Fore.RED + 'ALERT: File ' + output[0] + ' was removed!')
                    print(Style.RESET_ALL)
                

            file1.close()
            file2.close()

            time.sleep(1)

    except KeyboardInterrupt:
        print('Monitoring stopped')
        os.remove('hash_check.txt')
        os.remove(tmp)
        pass


def main():
    try:
        while True:
            option = input(
                'Choose and option \n 1) Collect a new baseline and start monitoring \n 2) Begin monitoring with saved baseline\n')

            match option:
                case '1':
                    basepath = input('Enter directory path: ')
                    filename = input('Enter temporary baseline name: ')
                    hash_create(basepath, filename)
                    
                    monitor(basepath, filename)

                case '2':
                    basepath = input('Enter directory path: ')
                    filename = input('Enter baseline name: ')
                    monitor(basepath, filename)

                case _:
                    print('Unexpected input')

    except KeyboardInterrupt:
        print('\nExiting program...\n')
        sys.exit()

    except EOFError as e:
        print(e)
        print('\nExiting program...\n')

if __name__ == '__main__':
    main()