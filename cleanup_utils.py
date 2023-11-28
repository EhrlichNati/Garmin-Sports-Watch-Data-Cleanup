import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_and_first_digest_data(path):
    # TODO:low yield after loading screening(4% from all files). change loading trouble shooting.
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
    if filtered_frame.shape[0] == 0:
        raise Exception("Can't define a set of features. Too many 'unknown' and NaN values."
                        " Check if the frame is deprecated.")
    representative_row_series = filtered_frame.iloc[0].filter(like='Field')
    return [feature + ' [' + filtered_frame['Units ' + str(field).split(" ")[1]].iloc[0] + ']' for field, feature
            in representative_row_series.items()]



def common_feature(df_series, threshold):
    normalized_counts = df_series.value_counts(normalize=True)
    max_percent = normalized_counts.max()
    return normalized_counts.idxmax() if max_percent >= threshold else None


def calculate_distance_diff(current_idx, next_idx, frame):
    time_delta = frame.loc[next_idx, 'timestamp [s]'] - frame.loc[current_idx, 'timestamp [s]']
    speed = frame.loc[next_idx, 'enhanced_speed [m/s]']
    return speed * time_delta if not pd.isna(speed) and not pd.isna(time_delta) else 0


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
                series_to_mean = col_numeric.loc[prev_valid:next_valid].copy()
                col.loc[i] = series_to_mean.mean()
            elif prev_valid is not None:

                col.loc[i] = col.loc[prev_valid]
            elif next_valid is not None:
                col.loc[i] = col.loc[next_valid]




def find_high_correlation_columns(frame, min_curr=0.8):
    """ Finds and returns a list of column names with correlation above the threshold"""
    corr_matrix = frame.corr(method='kendall')
    print(corr_matrix.to_string())
    cols = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > min_curr:
                cols.add(corr_matrix.columns[i])
                cols.add(corr_matrix.columns[j])
    return list(cols)



def normalize_dataframe(df):
    """Normalizes the numeric columns of a pandas DataFrame."""

    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(df)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns, index=df.index)
    return normalized_df


def save_to_folder(frame, csv_name, folder_path):
    frame.to_csv(folder_path + '/' + csv_name + '.csv', index=False)
    return




