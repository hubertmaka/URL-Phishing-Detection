import matplotlib.pyplot as plt


class PlotTwoCat:
    def __init__(self, positive_cat: str, negative_cat: str,
                 title: str, pos_values: list[int], neg_values: list[int]) -> None:
        self.neg_values = neg_values
        self.pos_values = pos_values
        self._categories = [positive_cat, negative_cat]
        self._title = title
        self.index = range(len(self._categories))
        self.width = 0.45

    @property
    def categories(self) -> list[str]:
        return self._categories

    @property
    def title(self) -> str:
        return self._title

    def plot_by_categories(self) -> None:
        plt.figure(figsize=(12, 6))
        bars1 = plt.bar(
            self.index,
            self.pos_values,
            self.width,
            label='NON PHISH'
        )
        bars2 = plt.bar([
            self.index[0] + self.width,
            self.index[1] + self.width],
            self.neg_values, self.width,
            label='PHISH'
        )

        for bar1, bar2 in zip(bars1, bars2):
            y_val1 = bar1.get_height()
            plt.text(bar1.get_x() + bar1.get_width() / 2, y_val1, y_val1, va='bottom', ha='center')
            y_val2 = bar2.get_height()
            plt.text(bar2.get_x() + bar2.get_width() / 2, y_val2, y_val2, va='bottom', ha='center')

        plt.xlabel('Categories')
        plt.ylabel('Amount of probes')
        plt.title(self._title)
        plt.xticks([self.index[0] + self.width / 2, self.index[1] + self.width / 2], self._categories)
        plt.legend()

        plt.show()

