import pandas as pd


class FileAnalyzer:

    def __init__(self, filepath: str):
        self.filepath = filepath

    def _read_csv_file(self):
        df = pd.read_csv(self.filepath, index_col=0)
        return df

    def start(self):
        df = self._read_csv_file()
        df.index = pd.to_datetime(df.index)
        aggregated_values = df.resample('M').mean()
        aggregated_values.index = pd.to_datetime(aggregated_values.index).strftime('%Y-%m')
        return aggregated_values


if __name__ == "__main__":
    a_mean = FileAnalyzer('a.csv').start()
    b_mean = FileAnalyzer('b.csv').start()
    print(a_mean)
    print(b_mean)
