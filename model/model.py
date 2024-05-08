import pickle
import pandas as pd
from feature_extraction import FeatureExtraction
from sklearn.pipeline import Pipeline


class Model(FeatureExtraction):
    def __init__(self, url: str, path_to_model: str) -> None:
        super().__init__(url)
        self._path_to_model = path_to_model
        self._input_dataframe: pd.DataFrame = pd.DataFrame({'URL': [url]})
        self._extracted_mean = 59
        self._extracted_chars: dict[str: int] = self.count_characters()
        self._model: Pipeline

    def _extract_features(self) -> None:
        self._input_dataframe['URL_LENGTH'] = self.url_length
        self._input_dataframe['HAVE_IP'] = 1 if self.have_ip_address() else 0
        self._input_dataframe['LONGER_THAN_MEAN'] = 1 if self.url_longer_than(self._extracted_mean) else 0
        for key, val in self._extracted_chars.items():
            self._input_dataframe[key] = val
        self._input_dataframe['HAVE_HTTPS'] = 1 if self.have_https() else 0
        self._input_dataframe['ABNORMAL_URL'] = 1 if self.abnormal_url else 0
        self._input_dataframe['DIGITS_AMOUNT'] = self.count_digits()
        self._input_dataframe['LETTERS_AMOUNT'] = self.count_letters()
        self._input_dataframe['PATH_DEPTH'] = self.path_depth()
        self._input_dataframe['DOTS_IN_NETLOC'] = self.dots_in_netloc()
        self._input_dataframe['NETLOC_LEN'] = self.netloc_length()
        self._input_dataframe['HAVE_SHORTENING_PATTERNS'] = 1 if self.have_shortening_patterns() else 0
        self._input_dataframe['HAVE_WWW_PREFIX'] = 1 if self.have_www_in_netloc() else 0
        # self._input_dataframe['NUMBER_OF_SLASHES_IN_PATH'] = self.count_slashes_in_path()
        self._input_dataframe['NUMBER_OF_WORDS_IN_NETLOC'] = self.count_words_in_netloc()
        # self._input_dataframe['HAVE_JS_CODE'] = 1 if self.have_javascript_code() else 0

    def _load_model(self) -> None:
        with open(self._path_to_model, mode='rb') as file_handler:
            self._model = pickle.load(file_handler)

    def _preprocess(self) -> None:
        self._extract_features()
        self._input_dataframe.drop(columns=['URL'], inplace=True)
        self._load_model()

    def get_input_parameters(self) -> pd.DataFrame:
        return self._input_dataframe

    def predict(self) -> float:
        self._preprocess()
        return self._model.predict(self._input_dataframe)


