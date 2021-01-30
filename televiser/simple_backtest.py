import pandas as pd
import matplotlib.pyplot as plt

__all__ = ['SimpleBackTest']


class SimpleBackTest:

    def __init__(self, frame, message):

        self.frame = frame
        self.message = message

    def backtest(self) -> 'pd_frame':
        """
            Back test strategy. Criteria and Returns columns must be present in
            frame.

            arguments:
                frame: pd.DataFrame()

            returns:
                pd.DataFrame with a strategy outcome
        """

        local_frame = self.frame
        start_price = local_frame.Close.iloc[0]

        local_frame['MA24'] = local_frame.Close.rolling(24).mean()
        local_frame['Criteria'] = local_frame.Close > local_frame.MA24

        time_in_position = local_frame.Criteria.value_counts()

        local_frame['Returns'] = local_frame.Close.pct_change()
        local_frame['Buy&Hold'] = start_price * (1 + local_frame['Returns']).cumprod()
        local_frame['Strategy'] = start_price * (1 + ( local_frame['Criteria'].shift(1) * local_frame['Returns'] )).cumprod()

        return local_frame


    def plot_frame(self, frame):

        fig = plt.figure(figsize=(14, 8))
        plt.plot(frame['Buy&Hold'], label='Купить и держать')
        plt.plot(frame['Strategy'], label='Используя стратегию')
        plt.legend()
        plt.box(False)
        plt.savefig('foo.png')

        return open('foo.png','rb')


    def __call__(self):

        frame = self.backtest()
        return self.plot_frame(frame)
