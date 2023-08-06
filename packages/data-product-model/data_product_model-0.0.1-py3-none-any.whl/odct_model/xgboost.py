#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import warnings

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV

from .base_model import BaseModel

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve
import yaml

penalty, cs, tol = ['l1', 'l2'], np.logspace(-3, 5, num=9), [1e-6]
hyper_parameters = dict(C=cs, penalty=penalty, tol=tol)


class XGBoostModel(BaseModel):
	"""This is a wrapper for xgboost model."""
	def __init__(self, config_file='./working_dir/data/config/models/xgboost_model.yaml'):
		print('XGBoostModel constructor')
		super().__init__(config_file)
		self.model = None
		self.model_name = self.parsed_config['model_description']['model_name']
		self.label_col_name = self.parsed_config['model_description']['label_col_name']
		
	def model_setup(self,list_min_samples_split=True,list_min_samples_leaf=True):
		if self.parsed_config['model_description']['hyper_parameter_tuning'] is True:
			print("Starting creating tuning parameters")
			self.root_parameters = self.parsed_config['model_hyper_tuning']

			#Train the xgboost model and tweaking hyper parameter using cross validation and random search.
			# Number of trees in xgboost
			start_n_estimator = self.root_parameters['n_estimators']['start']
			end_n_estimator = self.root_parameters['n_estimators']['end']
			step_n_estimator = self.root_parameters['n_estimators']['start']
			n_estimators = [int(x) for x in np.linspace(start=start_n_estimator, 
														stop=end_n_estimator, num=step_n_estimator)]

			# Number of features to consider at every split
			max_features = self.root_parameters['n_estimators']['max_features']

			# Maximum number of levels in tree
			start_max_depth = self.root_parameters['n_estimators']['start']
			end_max_depth = self.root_parameters['n_estimators']['end']
			step_max_depth = self.root_parameters['n_estimators']['start']
			max_depth = [int(x) for x in np.linspace(start_max_depth, end_max_depth, 
													num=step_max_depth)]
			max_depth.append(None)

			# Minimum number of samples required to split a node
			if list_min_samples_split:
				min_samples_split = self.root_parameters['n_estimators']['min_samples_split']['list_number']
			else:
				start_min_samples_split = self.root_parameters['n_estimators']['start']
				end_min_samples_split = self.root_parameters['n_estimators']['end']
				step_min_samples_split = self.root_parameters['n_estimators']['start']
				min_samples_split = [int(x) for x in np.linspace(start=start_min_samples_split, 
														stop=end_min_samples_split, num=step_min_samples_split)]

			# Minimum number of samples required at each leaf node
			if list_min_samples_leaf:    			
				min_samples_leaf = self.root_parameters['n_estimators']['min_samples_leaf']['list_number']
			else:
				start_min_samples_leaf = self.root_parameters['n_estimators']['start']
				end_min_samples_leaf = self.root_parameters['n_estimators']['end']
				step_min_samples_leaf = self.root_parameters['n_estimators']['start']
				min_samples_leaf = [int(x) for x in np.linspace(start=start_min_samples_leaf, 
														stop=end_min_samples_leaf, num=step_min_samples_leaf)]

			# Method of selecting samples for training each tree
			bootstrap = self.root_parameters['n_estimators']['bootstrap']

			#Set Resource
			n_jobs = self.root_parameters['n_estimators']['n_jobs']
			# Create the random grid
			random_grid = {'n_estimators': n_estimators,
						   'max_features': max_features,
						   'max_depth': max_depth,
						   'min_samples_split': min_samples_split,
						   'min_samples_leaf': min_samples_leaf,
						   'bootstrap': bootstrap}

			self.model = xgb.XGBClassifier()

			# Random search of parameters, using 5 fold cross validation,
			# search across randomly 100 different combinations
			if self.root_parameters['n_estimators']['type'] == 'random':
				
				self.search_method = RandomizedSearchCV(estimator=self.model,
														param_distributions=random_grid,
														n_iter=1,
														cv=5,
														verbose=5,
														random_state=42,
														n_jobs=n_jobs)
			else:
				self.search_method = GridSearchCV(estimator=self.model,
													param_distributions=random_grid,
													n_iter=1,
													cv=5,
													verbose=5,
													random_state=42,
													n_jobs=n_jobs)

		else:
			param_init = {}
			for k,v in self.parsed_config['model_parameters'].items():
				param_init[k] = v
			print(param_init)

			self.model = xgb.XGBClassifier(**param_init)

	def model_train(self):
		# Train model using hyper parameter tuning with grid search and cross validate
		if self.parsed_config['model_description']['hyper_parameter_tuning'] is True:
			# Fit the random search model
			self.search_method.fit(self.df_train_feature, self.df_train_label)

			print("The best hyper parameter: ", self.search_method.best_params_)

			# After we have the best hyper parameter, train the final model
			self.model = xgb.XGBClassifier(n_estimators=self.search_method.best_params_['n_estimators'],
												min_samples_split=self.search_method.best_params_[
														 'min_samples_split'],
												min_samples_leaf=self.search_method.best_params_[
														 'min_samples_leaf'],
												max_features=self.search_method.best_params_['max_features'],
												max_depth=self.search_method.best_params_['max_depth'],
												bootstrap=self.search_method.best_params_['bootstrap'])
			self.model.fit(self.df_train_feature, self.df_train_label)

		else:
			train_params=self.parsed_config['train_parameters']
			param_fit = {
				"eval_metric": train_params['eval_metric'],
				"early_stopping_rounds": train_params['early_stopping_rounds'],
				"verbose": train_params['verbose'],
				"eval_set": [(self.df_train_feature, self.df_train_label), (self.df_test_feature, self.df_test_label)]
			}

			# Train model here
			self.model.fit(self.df_train_feature, self.df_train_label, **param_fit)

	def model_eval(self,metric,x,y):
		number_plot = 0
		number_plot = number_plot + len([x if '_plot' in x else None for x in metric])
		if 'auc' in metric :
			# eval_data = pd.read_csv('./working_dir/data/eval/test.csv')
			# test_df = eval_data[self.df_train_feature.columns]
			# test_label = eval_data[self.label_col_name]
			pred = self.model.predict_proba(x)[:, 1]

			auc = metrics.roc_auc_score(y, pred)
			print('AUC : ', auc)

		if number_plot == 1:
			if 'cfs_plot' in metric:
				class_names = [0,1]
				plot_confusion_matrix(self.model, x, y,
												display_labels=class_names,
												cmap=plt.cm.Blues,
												normalize=None)
				plt.title('Confusion Matrix')

			if 'auc_plot' in metric:
				plot_roc_curve(self.model, x, y)
				plt.title('ROC')
				plt.show()

		else:
			fig, ax = plt.subplots(nrows=1, ncols=2,figsize = (20,8))
			fig.suptitle(f'Metric Plot')

			class_names = [0,1]
			plot_confusion_matrix(self.model, x, y,
											display_labels=class_names,
											cmap=plt.cm.Blues,
											normalize=None,ax=ax[0])
			ax[0].title.set_text('Confusion Matrix')

			plot_roc_curve(self.model, x, y,ax=ax[1])
			ax[1].title.set_text('ROC')
			fig.savefig('results.png')
			plt.show()



	def model_predict(self, df_features, prob=True):
		if prob:
			return self.model.predict_proba(df_features)
		else:
			return self.classifier.predict(df_features)

	def model_save(self, model_dir='./working_dir/data/models'):
		joblib.dump(self.classifier, os.path.join(model_dir, self.model_name))

	def model_load(self, model_dir='./working_dir/data/models'):
		pass

	def model_print(self, verbose):
		pass

	def pre_processing(self):
		pass

	def post_processing(self):
		pass