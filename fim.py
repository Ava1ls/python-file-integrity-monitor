import os
import sys
import time
import hashlib

HASH = hashlib.sha256()


def monitor():
    try:
        while True:
            print("monitoring")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Monitoring stopped")
        os.remove('baseline_tmp.txt')
        pass


def main():
    try:
        while True:
            option = input(
                "Choose and option \n 1) Collect a new baseline and start monitoring \n 2) Begin monitoring with saved baseline\n")

            match option:
                case "1":
                    # iterate trough user entered directory, create a "file-path | hash" pairs, begin monitoring
                    basepath = input("Enter directory relative path: ")
                    with os.scandir(basepath) as entries:
                        file_dictionary = []

                        for entry in entries:
                            if entry.is_file():
                                with open(entry, 'r') as file:
                                    f_entry = file.read()
                                calculated_hash = hashlib.sha256(
                                    f_entry.encode('utf-8')).hexdigest()

                                entry_path = os.path.abspath(entry) + "|" + calculated_hash
                                file_dictionary.append(entry_path)

                    try:
                        f_baseline = open("baseline_tmp.txt", "x")
                    except:
                        f_baseline = open("baseline_tmp.txt", "w")

                    for file in file_dictionary:
                        f_baseline.write(f"{file}"+'\n')

                    f_baseline.close()

                    monitor()

                case "2":
                    # iterate through user entered baseline, at each iteration create saved and recalculated hash pairs comparison, if != => ALERT
                    baseline_name = input(
                        "Enter baseline file name located in the same directory as a script file: ")
                    
                    with open(baseline_name, 'r') as file:
                        pass

                    monitor()
                case _:
                    print("Unexpected input")

    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit()

    except EOFError as e:
        print(e)
        print("Exiting program...")

if __name__ == '__main__':
    main()