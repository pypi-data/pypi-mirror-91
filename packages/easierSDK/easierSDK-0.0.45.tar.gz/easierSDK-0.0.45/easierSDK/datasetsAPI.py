#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.

import minio
from minio import Minio
import urllib3
import os
import subprocess
from typing import List
import random
import string
import shutil

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.feature_selection import chi2, f_classif, mutual_info_classif
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from easierSDK.classes.categories import Categories
from easierSDK.classes.dataset_metadata import DatasetMetadata

import json

class DatasetsAPI():
    """Class to control the Datasets API of EasierSDK.
    """

    _GLOBAL = 'global'
    _DATASETS = 'datasets'
    _BASE_DATASET_PATH = './datasets/'
    _MAX_FOLDER_SIZE = 2000000000 # Kbytes = 2G
    _MAX_FOLDER_SIZE_STR = '2GB'

    def __init__(self, minio_client, minio_bucket_public, minio_bucket_private):
        """Constructor for the DatasetsAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            minio_bucket_public (str): Name of the public bucket of the user.
            minio_bucket_private (str): Name of the private bucket of the user.
        """
        if not os.path.isdir(self._BASE_DATASET_PATH): os.mkdir(self._BASE_DATASET_PATH)
        self.minio_client = minio_client
        self.minio_bucket_public = minio_bucket_public
        self.minio_bucket_private = minio_bucket_private

    def _print_datasets(self, repo_name:str, category:Categories=None):
        """List datasets are under a specific repository and under a specific category.

        Args:
            repo_name (str): Name of the repository.
            category (Categories, optional): Category of the datasets to list. Defaults to None to show the datasets under every category.
        """
        if category:
            objects = self.minio_client.list_objects(repo_name, prefix=self._DATASETS + '/' + category.value, recursive=True)
        else:
            objects = [] 
            for category in Categories:
                objects += self.minio_client.list_objects(repo_name, prefix=self._DATASETS + '/' + category.value, recursive=True)
        
        already_printed = []
        row_format ="{:<30}" * 4
        for item in objects:
            repo_name = item.bucket_name
            name = item.object_name.split('/')[2]
            cat = item.object_name.split('/')[1]
            if [name, cat] in already_printed:
                continue
            already_printed.append([name, cat])
            size = item.size
            print(row_format.format(*[repo_name, cat, name, size]))
    
    def show_datasets(self, repo_name:str=None, category:Categories=None):
        """Show which datasets are under a specific repository and under a specific model Category.

        Args:
            repo_name (str, optional): Name of the repository to list datasets. Defaults to None to show all available repositories.
            category (Categories, optional): Category of the model. Defaults to None to show all datasets under each Category.
        """
        row_format ="{:<30}" * 4
        print(row_format.format(*['Repository', 'Category', 'Name', 'Size']))
        if repo_name is None:
            for repo in self.minio_client.list_buckets():
                self._print_datasets(repo.name, category)
        else:
            self._print_datasets(repo_name, category)
        

    def show_dataset_info(self, repo_name:str, category:Categories, dataset_name:str) -> DatasetMetadata:
        """Show metadata information of a specific dataset.

        Args:
            repo_name (str): Name of the repository that contains the dataset.
            category (Categories): Category that contains the dataset.
            dataset_name (str): Name of the dataset.

        Returns:
            DatasetMetadata: object with the dataset information.
        """
        # 1. Check bucket exists
        if not self.minio_client.bucket_exists(repo_name):
            print('[ERROR] Repository name does not exist. Please check and try again')
            return None
        # 2. Download file
        filename = self._DATASETS + '/' + category.value + '/' + dataset_name + '/' + 'metadata.json'

        local_file = './datasets/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_file)
        except minio.error.NoSuchKey as ex:
            print('[ERROR] Wrong dataset name or category, please check and try again.')
            return None
        # 3. Read file and format metadata
        with open(local_file, 'r') as f:
            metadata = DatasetMetadata(json.load(f))
            metadata.pretty_print()

        if os.path.exists(local_file):
            os.remove(local_file)
        return metadata

    def download(self, repo:str, category:Categories, dataset_name:str, path_to_download:str) -> bool:
        """Downloads a dataset and its attached objets in a specific path.

        Args:
            category (Categories): Category that contains the dataset.
            dataset_name (str): Name of the dataset.
            path_to_download (str): Local path in which to store all files.
            repo (str): Name of the repository that contains the dataset.
        Returns:
            bool: True if all files have been downloaded correctly, False if some file gave error.
        """
        # 1. Check if bucket exists
        if not self.minio_client.bucket_exists(repo):
            print('[ERROR] Wrong repo name. Please check and try again')
            return False
        # 2. Check if dataset exists
        filename = self._DATASETS + '/' + category.value + '/' + dataset_name + '/'
        object_list = self.minio_client.list_objects(repo, prefix=filename, recursive=True)
        has_items = False
        # 3. Download
        for obj in object_list:
            if not obj.is_dir:
                has_items = True
                self.minio_client.fget_object(repo, obj.object_name, path_to_download+'/'+obj.object_name)
        if not has_items:
            print('[ERROR] Could not find file. Please check parameters and try again.')
            return False
        # 4. If there are no problems, return True
        return True

    def _get_random_string(self) -> str:
        """Returns a random string.

        Returns:
            str: random string
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(1, 16))) 

    def store(self, dataset_name:str, dataset_path:str) -> str:
        """Compress the dataset's files to a compressed file.

        Args:
            dataset_name (str): name of dataset to store
            dataset_path (str): path where the dataset files are stored

        Returns:
            str: path in which the compressed file was stored.
        """
        old_dir = os.getcwd()
        os.chdir(dataset_path)
        subprocess.call(['tar', '-czf', dataset_name + '.tar.gz', "."])
        os.chdir(old_dir)
 
        return dataset_path

    def upload(self, category:Categories, dataset_name:str, local_path:str, metadata:DatasetMetadata, public:bool=False) -> bool:
        """Upload a dataset and its attached elements to the user's repository.

        Args:
            category (Categories): Category that contains the model.
            dataset_name (str): name of the dataset.
            local_path (str): root folder for the dataset. All the files under it will be uploaded as a tar.gz compresed file.
            metadata (DatasetMetadata): metadata of the dataset.
            public (bool, optional): Whether to upload the dataset in the public version of the repository. Defaults to False.

        Returns:
            bool: True if all files have  been uploaded correctly, False if some file gave error.
        """
        # Check path exists
        if not os.path.isdir(local_path):
            print('[ERROR] Path does not exist. Please save it and then upload again.')
            return False
        # Check folder size is not too big (parametrized)
        size = subprocess.check_output(['du','-sx', local_path]).split()[0].decode('utf-8')
        if int(size) > self._MAX_FOLDER_SIZE:
            print('[ERROR] Folder size too big. Current folder size is {}KB and max upload size is {}'.format(size, self._MAX_FOLDER_SIZE_STR))
            return False
        
        # Store and compress dataset files into a tar.gz
        self.store(dataset_name, local_path)
        
        # Dump metadata into file
        metadata.dump_to_file(local_path)

        path = '/tmp/' + self._get_random_string()
        while os.path.isdir(path): path += self._get_random_string()
        os.mkdir(path)

        subprocess.call(['mv', local_path + "/" + dataset_name + '.tar.gz', path])
        subprocess.call(['mv', local_path + "/" + 'metadata.json', path])

        # Upload all files in the path
        minio_path = 'datasets/' + category.value + '/' + dataset_name
        error = False
        
        if public:
            bucket = self.minio_bucket_public
        else:
            bucket = self.minio_bucket_private
        
        # Create bucket if doesn't exist
        if not self.minio_client.bucket_exists(bucket): self.minio_client.make_bucket(bucket, location='es')
        
        for f in os.listdir(path):
            try:    
                file_path = (minio_path + "/" + f)
                a, b =self.minio_client.fput_object(bucket, file_path, path + '/' + f)
            except Exception as ex:
                print('[ERROR] Unknown error uploading file {}: {}'.format(f, ex))
                error = True
        shutil.rmtree(path, ignore_errors=True)
        if error: 
            print('Finished uploading dataset with some errors.')
            return False
        else:
            print('Finished uploading dataset with no errors.')
            return True
    
    def load_csv(self, local_path:str, separator:str=';') -> pd.DataFrame:
        """Loads a CSV file into a pandas.DataFrame.

        Args:
            local_path (str): path of the CSV file.
            separator (str, optional): CSV file separator. Defaults to ';'.

        Returns:
            pd.DataFrame: pandas.DataFrame with the loaded dataset.
        """
        df = pd.read_csv(filepath_or_buffer=local_path, sep=separator)
        return df

    def train_test_split_data(self, dataframe_global:pd.DataFrame, labels, ratio:float=0.8):
        """
            Reads dataframe and scales data according to the configuration.
            Once scaled, data is splited into training and testing and returned.
        """
        
        split = int(len(dataframe_global.values) * float(ratio))

        x_train = dataframe_global.values[:split, :]  # First part of the array for testing
        x_test = dataframe_global.values[split:, :]  # Last for validating
    
        y_train = np.array(labels[:split])
        y_test = np.array(labels[split:])

        return x_train, y_train, x_test, y_test


    def scale_data(self, dataframe_global:pd.DataFrame, columns=None, scaler=None, ft_range=(0, 1), scaler_type='MinMax'):
        """
            Reads dataframe and scales data according to the configuration.
        """
        if columns:
            dataframe_global = dataframe_global.loc[:,columns] 
        # dataframe_shuffled = dataframe_global.sample(frac=1).reset_index(drop=True)

        data = dataframe_global.values.reshape(dataframe_global.values.shape[0], dataframe_global.values.shape[1])
        
        if scaler is None:
            if scaler_type == 'MinMax':
                scaler = MinMaxScaler(feature_range=ft_range)
            scaler = scaler.partial_fit(data)

        # transform
        data_scaled = scaler.transform(data)

        return pd.DataFrame(data_scaled), scaler

    def one_hot_encode_data(self, dataframe_global:pd.DataFrame, columns=None, labels=None, one_hot_encoder:OneHotEncoder=None, dtypes='object', dropna=True):
        """
            Reads dataframe and selects the columns that are not numbers. 
            Those columns are removed and put into a one_hot_encoder to convert them to numbers. 
            They are put back to the dataframe.
        """
        if labels:
            if isinstance(labels, str):
                dataframe_encode = dataframe_global.drop(columns=[labels])
            else:
                dataframe_encode = dataframe_global.drop(columns=labels)
        
        if columns:
            dataframe_encode = dataframe_global.loc[:,columns] 
        
        non_numeric = dataframe_encode.select_dtypes(include=dtypes)
        
        if not non_numeric.empty:

            if one_hot_encoder is None:
                one_hot_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
                non_numeric_encoded = one_hot_encoder.fit_transform(non_numeric.values)
            else:
                non_numeric_encoded = one_hot_encoder.transform(non_numeric.values)
            
            non_numeric_encoded = pd.DataFrame.from_records(non_numeric_encoded)
            
            numeric = dataframe_encode.select_dtypes(exclude=dtypes).reset_index()
            
            dataframe_encoded = pd.concat([numeric, non_numeric_encoded], axis=1)
            
            dataframe_global = pd.concat([dataframe_encoded, pd.DataFrame(dataframe_global.loc[:,labels])], axis=1)
            
        else:
            print("\tNo categorical data found with dtypes: " + str(dtypes))

        if dropna:
            dataframe_global = dataframe_global.dropna()

        return dataframe_global, one_hot_encoder
    
    def encode_labels(self, dataframe_global:pd.DataFrame, labels=None, label_encoder:LabelEncoder=None, dtype='int32'):
        """
            Uses a label encoder to encode a list of classes into numbers. Then transforms the array
            into a matrix of 1s and 0s. If any of parameters classes and label_encoder is provided,
            it/they is/are not stored as class' instance attributes. 
        """

        y = dataframe_global.loc[:,labels]

        if label_encoder is None:
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)
        
            return self.to_categorical(y), label_encoder
        else:
            y = label_encoder.transform(y)   

            return self.to_categorical(y, dtype=dtype), label_encoder

    def to_categorical(self, y, num_classes=None, dtype='float32'):
        """Converts a class vector (integers) to binary class matrix.

        E.g. for use with categorical_crossentropy.

        # Arguments
            y: class vector to be converted into a matrix
                (integers from 0 to num_classes).
            num_classes: total number of classes.
            dtype: The data type expected by the input, as a string
                (`float32`, `float64`, `int32`...)

        # Returns
            A binary matrix representation of the input. The classes axis
            is placed last.
        """
        y = np.array(y, dtype='int')
        input_shape = y.shape
        if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
            input_shape = tuple(input_shape[:-1])
        y = y.ravel()
        if not num_classes:
            num_classes = np.max(y) + 1
        n = y.shape[0]
        categorical = np.zeros((n, num_classes), dtype=dtype)
        categorical[np.arange(n), y] = 1
        output_shape = input_shape + (num_classes,)
        categorical = np.reshape(categorical, output_shape)
        return categorical

    def convert_to_timeseries(self, df:pd.DataFrame, prev_measures:int, num_forecasts:int, date_index:str, dataset_features:List[str], inference_features:List[str]) -> pd.DataFrame:
        """Converts a dataset into a timeseries variable.

        Args:
            df (pd.DataFrame): [description]
            prev_measures (int): [description]
            num_forecasts (int): [description]
            date_index (str): [description]
            dataset_features (List[str]): [description]
            inference_features (List[str]): [description]

        Returns:
            pd.DataFrame: [description]
        """
        features = dataset_features + inference_features + [date_index]
        print(df)

        # Only consider features selected
        df = df[features]
        print(df)

        # Set date as index
        df = df.set_index(date_index)
        print(df)

        n_vars = df.shape[1]
        print(n_vars)

        cols, names = list(), list()

        for i in range(prev_measures, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
            print(names)
        
        for i in range(0, num_forecasts):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]

        agg = pd.concat(cols, axis=1)
        agg.columns = names
        agg.dropna(inplace=True)

        print(agg)


    def upload_timeseries(self, df: pd.DataFrame, category:Categories, dataset_name:str, metadata:DatasetMetadata=None, public:bool=False):
        """Uploads a dataset to the repository.

        Args:
            df (pd.DataFrame): [description]
            category (Categories): [description]
            dataset_name (str): [description]
            metadata (DatasetMetadata, optional): [description]. Defaults to None.
            public (bool, optional): [description]. Defaults to False.
        """
        pass

    def quick_analysis(self, df: pd.DataFrame, feature_to_predict: str, date_index: str=None, show_plt:bool=False):
        """Performs a quick analysis of the dataset and its features.

        Args:
            df (pd.DataFrame): [description]
            feature_to_predict (str): [description]
            date_index (str, optional): [description]. Defaults to None.
            show_plt (bool, optional): [description]. Defaults to False.
        """
        self.pearson_correlation(df, feature_to_predict, show_plt)
        self.feature_selection(df, feature_to_predict, date_index)

    def feature_selection(self, df: pd.DataFrame, feature_to_predict: str, date_index: str=None, show_plt: bool=False):
        """Performs feature selection techniques in the dataset.

        Args:
            df (pd.DataFrame): [description]
            feature_to_predict (str): [description]
            date_index (str, optional): [description]. Defaults to None.
            show_plt (bool, optional): [description]. Defaults to False.
        """
        X_features = list(df.columns)
        X_features.remove(feature_to_predict)
        if date_index:
            X_features.remove(date_index)
        X = df[X_features]
        Y = df[feature_to_predict]
        X_indices = np.arange(X.shape[-1])
        selector = SelectPercentile(f_classif, percentile=60).fit(X, Y)
        X_new = SelectPercentile(f_classif, percentile=60).fit_transform(X, Y)
        print(selector.scores_)
        scores_SelPer = -np.log10(selector.pvalues_)
        scores_SelPer /= scores_SelPer.max()

        print("Scores per feature with SelectPercentile, 60% percentile of features:")
        df_scores = pd.DataFrame(scores_SelPer.reshape(1,-1), columns=X.columns.values)
        try: 
            from IPython import display
            display.display(df_scores)
        except ModuleNotFoundError: 
            print(df_scores)

        if show_plt: 
            plt.figure(figsize=(35,12))
            plt.clf()
            plt.bar(X.columns.values, scores_SelPer, width=.2,
                    label=r'Univariate score ($-Log(p_{value})$)', color='darkorange',
                    edgecolor='black')

            plt.title("Comparing feature scores")
            plt.xlabel('Feature')
            plt.yticks(())
            plt.axis('tight')
            plt.legend(loc='upper right')
            plt.show()

    def pearson_correlation(self, df: pd.DataFrame, feature_to_predict:str, show_plt:bool=False):
        """Computes the pearson correlation of the features in the dataset.

        Args:
            df (pd.DataFrame): [description]
            feature_to_predict (str): [description]
            show_plt (bool, optional): [description]. Defaults to False.
        """
        # Pearson correlation
        cor = df.corr()
        if show_plt:
            plt.figure(figsize=(15,12))
            sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
            plt.show()

        cor_target = abs(cor[feature_to_predict])
        print("\nCorrelation of each feature with output variable:\n", cor_target)

        relevant_features = cor_target[cor_target>0.5]
        print("\nSelected highly correlated features:\n", relevant_features)