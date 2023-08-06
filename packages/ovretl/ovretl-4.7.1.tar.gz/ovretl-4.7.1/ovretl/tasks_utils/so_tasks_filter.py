import pandas as pd


def so_tasks_filter(tasks_df: pd.DataFrame) -> pd.DataFrame:
    return tasks_df.loc[tasks_df["so_id"].notnull(), :]
