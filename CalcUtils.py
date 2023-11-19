import pandas as pd

def calculate_distance_diff(current_idx, next_idx, frame):
    time_delta = frame.loc[next_idx, 'timestamp [s]'] - frame.loc[current_idx, 'timestamp [s]']
    speed = frame.loc[next_idx, 'enhanced_speed [m/s]']
    return speed * time_delta if not pd.isna(speed) and not pd.isna(time_delta) else 0




