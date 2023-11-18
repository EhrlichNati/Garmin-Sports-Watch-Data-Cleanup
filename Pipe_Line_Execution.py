import os
import CleanUtils as clu
import Processing as pro

def run_clean(data_folder_path, processed_folder_path=False):
    files_names = os.listdir(data_folder_path)
    files_path = [data_folder_path + '/' + file_name for file_name in files_names]
    file_index = 1

    for path in files_path:
        frame = clu.load_and_first_digest_data(path)
        if frame.empty:
            print(f"Empty DataFrame, check encoding or record existence in pre processed data")
            continue
        print(path.split("/")[-1])
        initial_clean_frame = pro.clean_non_info_col(frame)
        frame_features_list = clu.create_features_list(initial_clean_frame)
        transformed_frame = pro.transform_frame(initial_clean_frame, frame_features_list)
        imputed_frame = pro.imputation(transformed_frame)
        file_index += 1
        if processed_folder_path:
            clu.save_to_folder(imputed_frame, "clean_frame, " + f'{file_index}', processed_folder_path)
    return imputed_frame


run_clean()


