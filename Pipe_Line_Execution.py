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

        # Process # BTW, sklrean has a pipeline class https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
        initial_clean_frame = pro.clean_non_info_col(frame)
        transformed_frame = pro.transform_frame(initial_clean_frame) # TODO: can you change the name of this function to something more meaningful?
        imputed_frame = pro.imputation(transformed_frame)

        # Optional save
        if processed_folder_path:
            clu.save_to_folder(imputed_frame, "clean_frame, " + f'{file_index}', processed_folder_path)
            file_index += 1

    return imputed_frame # not sure why are you processing each file but return only the last


# a better way to do so is,
# if __name__ == "__main__":
#   run_clean()
# if you don't do it like this, when someone only import this file, the run_clean() will run.
run_clean() # add here data_folder_path



# note the convision in python is that file names are snake_case.py and 
# class names are CammelCase, https://stackoverflow.com/a/42127721, so i would've rename the files.
