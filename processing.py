import cleanup_utils as clu
import calculation_utils as cal
from sklearn.impute import KNNImputer
import pandas as pd

def clean_non_info_col(frame):
    """After splitting(def split(data)), clean columns with unknown features or NaN values.
    because of lack of full alignment of rows and missing values,
    the method pick the common value using def common_value."""

    features_columns = [col for col in frame.columns if 'Field' in col]
    for col in features_columns:

        """Return common if above 80% of the values"""
        feature = clu.common_feature(frame[col])
        if (feature is None) or (feature == 'unknown'):
            frame.drop(columns=[col], inplace=True)

            """ Drop the subsequent units and value columns from (field, value, unit) block"""
            val, num = col.split(' ')
            headlines = (lambda pre: pre + ' ' + num, ['Value', 'Units'])
            filtered_columns = [headline for headline in headlines if headline in frame.columns]
            frame.drop(columns=filtered_columns, inplace=True)
    return


def arrange_features_columns(frame):
    """Iterate over rows and append the features and their values to dictionary.
         else append None value, to be imputed later with def imputation(frame):
    """
    features_list = clu.create_features_list(frame)

    dictionary = {}
    for index_row, row_series in frame.iterrows():
        for index, feature in enumerate(features_list):
                value = row_series.filter(like='Value').iloc[index]
                if feature in dictionary:
                    if str(feature).split(' ')[0] in row_series.values:
                        dictionary[feature].append(value)
                    else:
                        dictionary[feature].append(None)
                else:
                    dictionary[feature] = [value]
    return pd.DataFrame.from_dict(dictionary).dropna(axis=1, thresh=frame.shape[0]*0.9)



def imputation(frame):

    if frame.empty:
        raise ValueError("Input DataFrame is empty.")

    """Using KNN Imputation on columns that have high correlation"""

    knn_cols = ['heart_rate [bpm]', 'cadence [rpm]', 'fractional_cadence [rpm]', 'enhanced_speed [m/s]']
    knn_imp = KNNImputer(n_neighbors=30)
    existing_knn_cols = [col for col in knn_cols if col in frame.columns]
    existing_knn_cols.sort()


    """Impute location and altitude with the assumption that they didnt changed from the closest recording"""
    if existing_knn_cols:
        frame[existing_knn_cols] = pd.DataFrame(knn_imp.fit_transform(frame[existing_knn_cols]), columns=existing_knn_cols, index=frame.index).round(3)
    position_cols = ['position_lat [semicircles]', 'position_long [semicircles]', 'enhanced_altitude [m]']
    for col in position_cols:
        if col in frame.columns:
            clu.custom_fill(frame[col])

    """Impute distance by simple calculation, using time and speed data.
     adding the diff to the prev or subtracting diff to forward complete cells"""

    if 'distance [m]' in frame.columns and 'timestamp [s]' in frame.columns and 'enhanced_speed [m/s]' in frame.columns:
        for i in range(len(frame)):
            if pd.isna(frame.loc[i, 'distance [m]']):
                forward_filled = False
                for j in range(i, len(frame)):
                    if not pd.isna(frame.loc[j, 'distance [m]']):
                        distance_diff = cal.calculate_distance_diff(j - 1, j, frame)
                        frame.loc[j, 'distance [m]'] = frame.loc[j - 1, 'distance [m]'] + distance_diff
                        forward_filled = True
                        break

                if not forward_filled:
                    for j in range(i - 1, -1, -1):
                        if not pd.isna(frame.loc[j, 'distance [m]']):
                            distance_diff = cal.calculate_distance_diff(j, j + 1, frame)
                            frame.loc[j, 'distance [m]'] = frame.loc[j + 1, 'distance [m]'] - distance_diff
                            break
    return frame

