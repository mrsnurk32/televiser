import pandas as pd
import matplotlib.pyplot as plt
from .indicators import get_indicator

__all__ = ['SimpleBackTest']


class SimpleBackTest:

    def __init__(self, frame, message):

        self.frame = frame
        self.message = message

    def backtest(self, local_frame) -> 'pd_frame':

        """
            Back test strategy. Criteria and Returns columns must be present in
            frame.

            arguments:
                frame: pd.DataFrame()

            returns:
                pd.DataFrame with a strategy outcome
        """

        start_price = local_frame.Close.iloc[0]

        time_in_position = local_frame.Criteria.value_counts()

        local_frame['Returns'] = local_frame.Close.pct_change()
        local_frame['Buy&Hold'] = start_price * (1 + local_frame['Returns']).cumprod()
        local_frame['Strategy'] = start_price * (1 + ( local_frame['Criteria'].shift(1) * local_frame['Returns'] )).cumprod()

        return local_frame


    def plot_frame(self, frame):

        """
            This method saves fig and returns bytes
        """

        fig = plt.figure(figsize=(14, 8))
        plt.plot(frame['Buy&Hold'], label='Купить и держать')
        plt.plot(frame['Strategy'], label='Используя стратегию')
        plt.legend()
        plt.box(False)
        plt.savefig('foo.png')

        return open('foo.png','rb')


    def __call__(self, indicator, kwargs=None):
        local_frame = get_indicator(indicator=indicator, frame=self.frame)
        frame = self.backtest(local_frame)
        return self.plot_frame(frame)
