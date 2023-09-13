import csv
import os


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def save_to_csv_file(list_of_dictionaries, file_path):
    if len(list_of_dictionaries) == 0:
        print("No data to save")
        return

    is_file_exist = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list_of_dictionaries[0].keys())
        if not is_file_exist:
            writer.writeheader()
        writer.writerows(list_of_dictionaries)
