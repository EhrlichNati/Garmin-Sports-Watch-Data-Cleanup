import os
import CleanUtils as clu
import Processing as pro

def run_clean(data_folder_path, processed_folder_path=False):
    files_names = os.listdir(data_folder_path)
    files_path = [data_folder_path + '/' + file_name for file_name in files_names]

    imputed_frame = None
    file_index = 1
    for path in files_path:
        frame = clu.load_and_first_digest_data(path) 
        if frame.empty:
            print(f"Empty DataFrame, check encoding or records existence in pre processed data")
            continue
            
        pro.clean_non_info_col(frame)
        pro.arrange_features_columns(initial_clean_frame)
        pro.imputation(transformed_frame)
        
        # Optional save
        if processed_folder_path:
            clu.save_to_folder(imputed_frame, "clean_frame, " + f'{file_index}', processed_folder_path)
            file_index += 1
    return frame 



if __name__ == "__main__":
   run_clean()

run_clean("Data/Before Processing")
