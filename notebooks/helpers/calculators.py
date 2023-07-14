import pandas as pd
from scipy import stats

rolling_columns_change_array = [
    "_3m_change",
    "_6m_change",
    "_12m_change",
    "_24m_change"
]

months_array = [
    "_3m",
    "_6m",
    "_12m",
    "_24m"
]


def calculate_pct_changes(dataframe: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Calculates the percentage changes and z-scores for the specified column in the given DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        col_name (str): The name of the column for which to calculate the changes and z-scores.

    Returns:
        pd.DataFrame: The updated DataFrame with the calculated changes and z-scores.
    """

    # Calculate percentage changes
    dataframe[f'{col_name}_3m_change'] = dataframe[col_name].pct_change(3)
    dataframe[f'{col_name}_6m_change'] = dataframe[col_name].pct_change(6)
    dataframe[f'{col_name}_12m_change'] = dataframe[col_name].pct_change(12)
    dataframe[f'{col_name}_24m_change'] = dataframe[col_name].pct_change(24)

    # Calculate z-scores for each rolling average

    for column in [f"{col_name}{change}" for change in rolling_columns_change_array]:
        z_scores = stats.zscore(dataframe[column].dropna())
        dataframe[column + '_z_score'] = pd.Series(z_scores, index=dataframe.index)
        # Calculate z-scores
        z_scores = stats.zscore(dataframe[f'{col_name}_3m_change'].dropna())
        dataframe[f'{col_name}_3m_z_score'] = pd.Series(z_scores, index=dataframe.index)

    return dataframe


def calculate_rolling_z_scores(dataframe: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Calculates the rolling z-scores for the specified column in the given DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        col_name (str): The name of the column for which to calculate the rolling z-scores.

    Returns:
        pd.DataFrame: The DataFrame with the rolling z-scores added for each specified horizon.
    """
    rolling_z_scores = pd.DataFrame()

    for horizon in [3, 6, 12, 24]:
        rolling_mean = dataframe[col_name].rolling(window=horizon).mean()
        rolling_std = dataframe[col_name].rolling(window=horizon).std()
        z_scores = (dataframe[col_name] - rolling_mean) / rolling_std
        rolling_z_scores[f'{col_name}_{horizon}m_z_score'] = z_scores
        rolling_z_scores[f'{col_name}_{horizon}m_mean'] = rolling_mean

    return rolling_z_scores


def calculate_rolling_difference(dataframe: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Calculates the rolling difference between the current value and the one from 3, 6, 12, and 24 months ago
    for the specified column in the given DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        col_name (str): The name of the column for which to calculate the rolling difference.

    Returns:
        pd.DataFrame: The DataFrame with the rolling difference added for each specified horizon.
    """
    rolling_diff = pd.DataFrame()

    for horizon in [3, 6, 12, 24]:
        diff = dataframe[col_name] - dataframe[col_name].shift(horizon)
        rolling_diff[f'{col_name}_{horizon}m_diff'] = diff

    return rolling_diff