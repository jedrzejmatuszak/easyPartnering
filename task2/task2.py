import pandas as pd
from pathlib import Path


def group_by_month(filepath: Path):
    df = pd.read_csv(filepath, index_col=0)
    df.index = pd.to_datetime(df.index)
    aggregated_values = df.resample('M').mean()
    aggregated_values.index = pd.to_datetime(aggregated_values.index).strftime('%Y-%m')
    return aggregated_values


def concatenate_two_files(filepath1: Path, filepath2: Path):
    file1 = pd.read_csv(filepath1, index_col=0)
    file2 = pd.read_csv(filepath2, index_col=0)
    concat_files = pd.concat([file1, file2.reindex(file1.index)], axis=1)
    concat_files.to_csv('c.csv')


if __name__ == "__main__":
    a_path = Path('a.csv')
    b_path = Path('b.csv')
    a_mean = group_by_month(a_path)
    b_mean = group_by_month(b_path)
    print(a_mean)
    print(b_mean)
    concatenate_two_files(a_path, b_path)
