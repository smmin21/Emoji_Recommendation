from gensim.models import fasttext
from gensim.test.utils import datapath
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from konlpy.tag import Kkma
from tqdm import tqdm
import statistics
import os
from django.conf import settings

class MyEmoji:
    def __init__(self):
        self.base_dir = settings.BASE_DIR
        # self.base_dir = "C:/Users/s_mmin/Desktop/text_class"
        self.model_path = os.path.join(self.base_dir, 'app', 'static/emoji/wiki.ko.bin')
        self.model = fasttext.load_facebook_vectors(datapath(self.model_path))
        self.df = self.give_data()
        self.kkma = Kkma()
        
    def give_data(self):
        df_json = pd.read_json(os.path.join(self.base_dir, 'app', 'static/emoji/embedding_lines.json'), orient = 'records', lines=True).reset_index()
        df_json.columns = ['index', 'id','emoji', 'explanation', 'kkma_nouns', 'ft_embedding']
        return df_json
    
    def cos_sim(self, A, B):
        return dot(A, B)/(norm(A)*norm(B))
    
    def return_answers_by_max(self, input):
        extract_nouns = self.kkma.nouns(input)
        input_embedding = [self.model[word] for word in extract_nouns]
        scores = []
        for _, row in self.df.iterrows():
            dis = [max([self.cos_sim(i, w) for i in input_embedding]) for w in row['ft_embedding']]
            scores.append(max(dis)) if dis else scores.append(0)
        self.df['score'] = scores
        df_sorted = self.df.sort_values(by='score', ascending=False)
        return df_sorted
    
    def return_answers_by_mean(self, input):
        extract_nouns = self.kkma.nouns(input)
        input_embedding = [self.model[word] for word in extract_nouns]
        scores = []
        for _, row in self.df.iterrows():
            dis = [self.cos_sim(i, w) for i in input_embedding for w in row['ft_embedding']]
            scores.append(statistics.mean(dis)) if dis else scores.append(0)
        self.df['score'] = scores
        df_sorted = self.df.sort_values(by='score', ascending=False)
        return df_sorted
    
    def find_emoji(self, input):
        r_mean = self.return_answers_by_mean(input)
        r_max = self.return_answers_by_max(input)
        r_mean['ordered_id'] = range(0, len(r_mean))
        r_max['ordered_id'] = range(0, len(r_mean))
        merged_df = r_mean[['id', 'emoji', 'explanation', 'ordered_id']].merge(r_max[['id', 'ordered_id']], on='id', how='outer')
        merged_df['sum_ordered'] = merged_df['ordered_id_x'] + merged_df['ordered_id_y']
        merged_df = merged_df.sort_values(by='sum_ordered', ascending=True)
        return merged_df.head()

if __name__ == '__main__':
    my_emoji = MyEmoji()
    while True:
        user_input = input("Enter text: ")
        if user_input.lower() == 'q': 
            break
        result = my_emoji.find_emoji(user_input)
        print(result)




