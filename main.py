from feature_extraction.feature_extraction import FeatureExtraction


class Main:
    @staticmethod
    def main() -> None:
        fe1 = FeatureExtraction("https://en.wikipedia.org/wiki")
        print(fe1._shortening_pattern)


if __name__ == '__main__':
    Main.main()
