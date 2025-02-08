import matplotlib.pyplot as plt
import pandas as pd


class DataReader:
    def __init__(self):
        self.grouped_df = None

    # функция для конвертации CSV файла в датафрейм Pandas
    def data_converter(self):
        path_to_file = "datasets/Аналитик — тестовое задание - data.csv"
        df = pd.read_csv(path_to_file, usecols=["event_date", "is_attend"])
        grouped_df = df.groupby("event_date", dropna=False).sum()
        self.grouped_df = grouped_df
    # --- --- ---

    # функция для добавления значений на столбцы диаграммы (сколько чел. пришло за конкретную дату)
    def addlabels(self, x, y):
        for i in range(len(x)):
            plt.text(i, y.iloc[i] // 2, y.iloc[i], ha='center')
    # --- --- ---

    # функция для построения и отображения столбчатой диаграммы по сгруппированному датасету
    def graph_maker(self):
        self.data_converter()
        plt.bar(self.grouped_df.index, self.grouped_df["is_attend"])
        plt.xticks(rotation=90)
        plt.ylabel("Посетили за день (чел.)")
        plt.xlabel("Дата")
        plt.tight_layout()
        self.addlabels(self.grouped_df.index, self.grouped_df["is_attend"])
        plt.show()
    # --- --- ---


if __name__ == '__main__':
    data_reader = DataReader()
    data_reader.graph_maker()
