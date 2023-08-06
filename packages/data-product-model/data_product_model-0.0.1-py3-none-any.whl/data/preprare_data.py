import os
import random
import pandas as pd
import re
from sklearn.model_selection import train_test_split

pd.options.display.max_columns = 100


class HiRODPrepro:
    """This class is for preprocess purpose.
    It can run train/test split or save results for further processing. This is a very simple example.
    """
    def __init__(self, raw_train_data='./working_dir/data/train.csv',
                 label_name='is_failed'):
        """Constructor."""
        self.train_data = pd.read_csv(raw_train_data)
        self.df_train_feature = None
        self.df_train_label = None
        self.df_test_feature = None
        self.df_test_label = None

        self.label_name = label_name

    def train_test_preparing(self, test_percentage=0.2,
                             save_train_test=False,
                             train_test_dir='./working_dir/data/train_test_split',
                             train_file_feature='train_x.csv',
                             train_file_label='train_y.csv',
                             test_file_feature='test_x.csv',
                             test_file_label='test_y.csv'
                             ):
        """Train/test splitting"""
        print('Feature columns:')
        print(self.train_data.columns)
        self.df_train_feature, self.df_test_feature, self.df_train_label, self.df_test_label = train_test_split(
            self.train_data,
            self.train_data[self.label_name],
            test_size=test_percentage,
            random_state=random.randint(1, 10000))

        columns = self.df_train_feature.columns
        self.df_train_feature = self.df_train_feature.drop(self.label_name)
        self.df_test_feature = self.df_test_feature.drop(self.label_name)

        if save_train_test:
            self.df_train_feature.to_csv(os.path.join(train_test_dir, train_file_feature), header=True, index=False)
            self.df_train_label.to_csv(os.path.join(train_test_dir, train_file_label), header=True, index=False)
            self.df_test_feature.to_csv(os.path.join(train_test_dir, test_file_feature), header=True, index=False)
            self.df_test_label.to_csv(os.path.join(train_test_dir, test_file_label), header=True, index=False)