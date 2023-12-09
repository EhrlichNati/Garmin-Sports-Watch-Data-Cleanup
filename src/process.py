import os
from src.config_load import config
import src.cleanup_utils as clu
import src.processing as pro


def reformat_files():
    # Prepare paths of all row files
    input_folder_with_raw_files = config['data_folders']['input_data']
    output_folder_processed_files = config['data_folders']['output_data']
    files_names = os.listdir(input_folder_with_raw_files)
    files_path = [input_folder_with_raw_files + '/' + file_name for file_name in files_names]

    for i, path in enumerate(files_path):
        frame = clu.load_and_first_digest_data(path)
        if frame.empty:
            print(f"The DataFrame is devoid of data following standard cleanup procedures - the file lacks useful information.")
            continue

        # Process
        pro.clean_non_info_col(frame)
        transformed_frame = pro.arrange_features_columns(frame)
        pro.imputation(transformed_frame)


        clu.save_to_folder(transformed_frame, "clean_frame, " + f'{i}', output_folder_processed_files)

    return

