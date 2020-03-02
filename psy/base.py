import os
from abc import ABCMeta, abstractmethod


class DataProcessor(metaclass=ABCMeta):
    """Base processor to be used for all preparation."""
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    @abstractmethod
    def read(self):
        """Read raw data."""

    @abstractmethod
    def process(self):
        """Processes raw data. This step should create the raw dataframe with all the required features. Shouldn't implement statistical or text cleaning."""

    @abstractmethod
    def save(self):
        """Saves processed data."""


class Trainer(metaclass=ABCMeta):
    """Base trainer to be used for all models."""

    def __init__(self, directory):
        self.directory = directory
        self.model_directory = os.path.join(directory, 'models')

    @abstractmethod
    def preprocess(self):
        """This takes the preprocessed data and returns clean data. This is more about statistical or text cleaning."""

    @abstractmethod
    def set_model(self):
        """Define model here."""

    @abstractmethod
    def fit_model(self):
        """This takes the vectorised data and returns a trained model."""

    @abstractmethod
    def generate_metrics(self):
        """Generates metric with trained model and test data."""

    @abstractmethod
    def save_model(self, model_name):
        """This method saves the model in our required format."""


class Predict(metaclass=ABCMeta):
    """Base predictor to be used for all models."""

    def __init__(self, directory):
        self.directory = directory
        self.model_directory = os.path.join(directory, 'models')

    @abstractmethod
    def load_model(self):
        """Load model here."""

    @abstractmethod
    def preprocess(self):
        """This takes the raw data and returns clean data for prediction."""

    @abstractmethod
    def predict(self):
        """This is used for prediction."""


class BaseDB(metaclass=ABCMeta):
    """ Base database class to be used for all DB connectors."""
    @abstractmethod
    def get_connection(self):
        """This creates a new DB connection."""
    @abstractmethod
    def close_connection(self):
        """This closes the DB connection."""
