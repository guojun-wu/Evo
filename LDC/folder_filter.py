import os
import re
from datetime import datetime, timedelta
import pandas as pd

class Folder_filter:
    def __init__(self, directory_path, reference_path):
        self.directory_path = directory_path
        self.reference_path = reference_path
        self.languages = ['de', 'en', 'es', 'it', 'zh']
    
    def read_file(self, ref_file, hyp_file):
        with open(ref_file, 'r') as f:
            ref_lines = f.readlines()
        with open(hyp_file, 'r') as f:
            hyp_lines = f.readlines()
        return ref_lines, hyp_lines
    
    def filter_folders(self):
        # Find out folders that contain files with different number of lines than the reference file.
        invalid_folders = []
        for folder in os.listdir(self.directory_path):
            folder_path = os.path.join(self.directory_path, folder)
            if not os.path.isdir(folder_path):
                continue
            for filename in os.listdir(folder_path):
                if not filename.endswith('.txt'):
                    continue
                file_path = os.path.join(folder_path, filename)
                src_lang = filename[:2]
                tgt_lang = filename[4:6]
                if src_lang in self.languages and tgt_lang in self.languages:
                    ref_file = os.path.join(self.reference_path, 'amr-' + tgt_lang + '.txt')
                    ref_lines, hyp_lines = self.read_file(ref_file, file_path)
                    for line in hyp_lines:
                        if line == '\n':
                            # print(f"Error: {file_path} contains empty lines.")
                            invalid_folders.append(folder)
                            break
                    if len(ref_lines) != len(hyp_lines):
                        # print(f"Error: {file_path} has different number of lines.")
                        invalid_folders.append(folder)
                        break
                    
        return invalid_folders

    def sort(self, with_date=False):

        folder_names = os.listdir(self.directory_path)
        invalid_folders = self.filter_folders()
        folder_names = [foldername for foldername in folder_names if foldername not in invalid_folders]
        print(f"Number of valid folders: {len(folder_names)}")
        date_folders = [foldername for foldername in folder_names if re.match(r'\w+-\d{2}-\d{4}', foldername)]
        date_objects = []
        for foldername in date_folders:
            try:
                date_obj = datetime.strptime(foldername, '%B-%d-%Y')
                date_objects.append((foldername, date_obj))
            except ValueError:
                pass  # Handle folders with incorrect date formats

        sorted_folders = sorted(date_objects, key=lambda x: x[1])

        # save sorted folders to a file
        sorted_folders = pd.DataFrame(sorted_folders)
        sorted_folders.columns = ['folder_name', 'date']

        return sorted_folders
