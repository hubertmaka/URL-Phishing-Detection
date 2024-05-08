from feature_extraction.feature_extraction import FeatureExtraction
from automation_utils.download_automation_script import DownloadDataAutomationScript
from saved_models.model import Model
import os


class Main:
    MAX_PAGE = 6409

    @staticmethod
    def main() -> None:
        my_url = 'https://phishtank.org/phish_search.php'
        # path_to_non_phishing_file = 'datasets/non-phishing-urls-phishtank.csv'
        # download_manager = DownloadDataAutomationScript(my_url, path_to_non_phishing_file)
        # download_manager.scrap_data(0, Main.MAX_PAGE)
        model = Model('https://phishtank.org/phish_search.php', os.path.join('saved_models', 'random_forest_model'))
        print(model.predict())


if __name__ == '__main__':
    Main.main()
