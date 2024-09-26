import pandas as pd
import os
from folder_filter import Folder_filter
import argparse

def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # Remove the newline character at the end of each line
    lines = [line.strip() for line in lines]
    return lines

def select_folders(directory_path, reference_path):
    folder_filter = Folder_filter(directory_path, reference_path)
    sorted_folders = folder_filter.sort()

    num_folders_to_select = 65

    # Calculate the interval between the first and last date
    first_date = sorted_folders.iloc[0]['date']
    last_date = sorted_folders.iloc[-1]['date']
    date_interval = (last_date - first_date) / (num_folders_to_select - 1)

    # Select folders evenly distributed over time
    selected_folders = []
    current_date = first_date
    for _ in range(num_folders_to_select):
        nearest_date_index = (sorted_folders['date'] - current_date).abs().idxmin()
        selected_folders.append(sorted_folders.iloc[nearest_date_index])
        current_date += date_interval

    selected_folders_df = pd.DataFrame(selected_folders)
    # print number of columns
    print(selected_folders_df.shape[0])

    return selected_folders_df['folder_name'].tolist()

   
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir_path', type=str, default='LDC/translation-files-new', help='path for the translation folders')
    parser.add_argument('-r', '--ref_path', type=str, default='LDC/amr-files', help='path for the reference files')
    args = parser.parse_args()

    directory_path = args.dir_path # Path to the directory containing the system outputs
    reference_path = args.ref_path # Path to the directory containing the reference files

    languages = ['de', 'en', 'es', 'it', 'zh']
    # Create a dictionary of dataframes for each language pair
    dataframes = {}
    for source_lang in languages:
        for target_lang in languages:
            if source_lang != target_lang:
                # Create a dataframe with two columns: source and target
                source_file = os.path.join(reference_path, 'amr-' + source_lang + '.txt')
                target_file = os.path.join(reference_path, 'amr-' + target_lang + '.txt')
                source = read_file(source_file)
                target = read_file(target_file)
                data = {'source': source, 'target': target}
                df = pd.DataFrame(data)
                
                # Store the dataframe in the dictionary with a key that represents the language pair.
                key = f"{source_lang}-{target_lang}"
                dataframes[key] = df
    
    # Select folders evenly distributed over time
    selected_folders = select_folders(directory_path, reference_path)

    for folder in selected_folders:
        print(f"Processing {folder}...")
        folder_path = os.path.join(directory_path, folder)

        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):
            if not filename.endswith('.txt'):
                continue
            file_path = os.path.join(folder_path, filename)

            src_lang = filename[:2]
            tgt_lang = filename[4:6]

            if src_lang in languages and tgt_lang in languages:
                key = f"{src_lang}-{tgt_lang}"
                dataframes[key][folder] = read_file(file_path)

    # Save the dataframes to csv files
    if not os.path.exists('data'):
        os.makedirs('data')
    for key in dataframes:
        df = dataframes[key]
        df.to_csv(f'data/{key}.csv', index=False)

if __name__ == '__main__':
    main()






    


    
    


