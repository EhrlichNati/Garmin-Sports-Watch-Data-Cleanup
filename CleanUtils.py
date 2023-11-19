import pandas as pd

def load_and_first_digest_data(path):

    try:
        data = pd.read_csv(path, encoding='utf-8', on_bad_lines='skip')
    except(FileNotFoundError, UnicodeDecodeError) as e:
        exception_type = type(e).__name__
        print(f"An error occurred: {exception_type}")
        return pd.DataFrame([])

    data = data[data['Message'].isin(['record']) & ~data['Type'].isin(['Definition'])].reset_index(drop=True)
    columns_to_drop = ['Type', 'Local Number', 'Message']
    return data.drop(columns=columns_to_drop).dropna(axis=1, how='all')


def create_features_list(frame):
    """find series that have complete set of features, pick index=0 arbitrary """
    filtered_frame = frame[~frame.map(lambda cell: 'unknown' in str(cell) or pd.isna(cell)).any(axis=1)]
    if filtered_frame.shape[0] > 1:
        filtered_series = filtered_frame.iloc[0].filter(like='Field')
    else:
        raise Exception("Can't defined set of features. to much 'unknown' and None values."
                        "check if frame is deprecated")
    return [feature + ' [' + filtered_frame['Units ' + str(field).split(" ")[1]].iloc[0] + ']' for field, feature in filtered_series.items()]



def common_feature(df_series):
    normalized_counts = df_series.value_counts(normalize=True)
    max_percent = normalized_counts.max()
    return normalized_counts.idxmax() if max_percent >= 0.9 else None



def concat(frames_list):
    all_columns = list(set().union(*(frame.columns for frame in frames_list))).sort(reverse=True)
    adjusted_dfs = [df.reindex(columns=all_columns) for df in frames_list]
    return pd.concat(adjusted_dfs, ignore_index=True, sort=False)



def custom_fill(col):
    for i in range(len(col)):
        col_numeric = pd.to_numeric(col, errors='coerce')
        if pd.isna(col[i]):
            prev_valid = col_numeric.iloc[:i].last_valid_index()
            next_valid = col_numeric.iloc[i + 1:].first_valid_index()

            if prev_valid is not None and next_valid is not None:
                col.loc[i] = col_numeric.loc[prev_valid:next_valid].mean()
            elif prev_valid is not None:
                col.loc[i] = col.loc[prev_valid]
            elif next_valid is not None:
                col.loc[i] = col.loc[next_valid]


def save_to_folder(frame, csv_name, folder_path):
    frame.to_csv(folder_path + '/' + csv_name + '.csv', index=False)
    return




