import glob
import pandas as pd

class ListFile:
    def __init__(self, _folder:str = 'data', _format:str = 'csv'):
        self.folder = _folder
        self.format = _format
        self.list_file_data = self.__get_list_file()
        
    def __get_list_file(self):
        folder_path =  self.folder + '/*.' + self.format
        return glob.glob(folder_path)
    
class GlobalData:
    def __init__(self, _list_file:list):
        self.list_file = _list_file
        self.data = self.__get_data()
        self.data_words = self.__get_data_words()
    
    def __get_data(self):
        dataframes = []

        for file in self.list_file:
            df = pd.read_csv(file)
            df['source_file'] = file
            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)

        return combined_df
    def __get_data_words(self):
        words_data = []

        for i, row in self.data.iterrows():
            date = row['Дата визита']
            source_file = row['source_file']
            phrase = row['Поисковая фраза (Директ)']
            visits = row['Визиты']

            try:
                words = phrase.split()
            except:
                continue

            if phrase != "Не определено":
                for word in words:
                    words_data.append({
                        'date': date,
                        'source' : source_file,
                        'word': word,
                        'visits': visits
                    })
            else:
                words_data.append({
                        'date': date,
                        'source' : source_file,
                        'word': phrase,
                        'visits': visits
                    })
        
        words_df = pd.DataFrame(words_data)
        words_df['date'] = pd.to_datetime(words_df['date'])

        return words_df.groupby(['date', 'source', 'word'], as_index=False).sum()



