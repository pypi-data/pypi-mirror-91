import os
from collections import OrderedDict
from abc import ABC, abstractmethod
import yaml


class BaseModel(ABC):
    """This class is an abstract base class (ABC) for models."""

    def __init__(self, config_file):
        """Initialize the BaseModel class."""
        print ('BaseModel constructor')

        config_file = open(config_file)
        self.parsed_config = yaml.load(config_file, Loader=yaml.FullLoader)
        self.df_train_feature = None
        self.df_train_label = None
        self.df_test_feature = None
        self.df_test_label = None

    @abstractmethod
    def model_setup(self):
        """Load and print models
        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        pass

    @abstractmethod
    def model_train(self):
        """Train model."""
        pass

    @abstractmethod
    def model_eval(self):
        """Make models eval mode during test time"""
        pass

    @abstractmethod
    def model_predict(self):
        """Predict"""
        pass

    @abstractmethod
    def model_save(self, model_dir='./working_dir/data/models'):
        """Save all the models to the disk. """
        pass

    @abstractmethod
    def model_load(self, model_dir='./working_dir/data/models'):
        """Load all the models from the disk."""
        pass

    @abstractmethod
    def model_print(self, verbose):
        """Print the model parameters and it's architecture."""
        pass

    @abstractmethod
    def pre_processing(self):
        """Preprocess data.
        The code logic thoroughly depending on you.
        """
        pass

    @abstractmethod
    def post_processing(self):
        """Post processing."""
        pass

    @staticmethod
    def modify_commandline_options(parser, is_train):
        """Add new model-specific options, and rewrite default values for existing options.
        Parameters:
            parser          -- original option parser
            is_train (bool) -- whether training phase or predict phase.
        Returns:
            the modified parser.
        """
        return parser