from feature_extraction.feature_extraction import FeatureExtraction
from automation_utils.download_automation_script import DownloadDataAutomationScript


class Main:
    @staticmethod
    def main() -> None:
        my_url = 'https://phishtank.org/phish_search.php'
        file_to_path = 'datasets/non-phishing-urls-phishtank.csv'
        download_manager = DownloadDataAutomationScript(my_url, file_to_path)
        download_manager.scrap_data(0, 100)

        fe1 = FeatureExtraction("https://en.wikipedia.org/wiki")


if __name__ == '__main__':
    Main.main()
