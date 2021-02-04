import pandas as pd
import matplotlib.pyplot as plt
from .indicators import get_indicator
import numpy as np

__all__ = ['SimpleBackTest']


class SimpleBackTest:

    def __init__(self, frame, message,ticker):

        self.frame = frame
        self.message = message
        self.ticker = ticker

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
        local_frame['Strategy_returns'] = local_frame.Strategy.pct_change()

        return local_frame


    def plot_frame(self, frame, indicator_data):

        """
            This method saves fig and returns bytes
        """

        fig = plt.figure(figsize=(14, 8))
        plt.title(f'{self.ticker.upper()}  {indicator_data["title"]}')
        plt.plot(frame['Buy&Hold'], label='Купить и держать')
        plt.plot(frame['Strategy'], label='Используя стратегию')
        plt.legend()
        plt.box(False)
        plt.savefig('foo.png')

        return open('foo.png','rb')

    
    def evaluate(self, frame):

        strategy_net_income = frame.Strategy.iloc[-1] / frame.Strategy.iloc[1] -1
        asset_net_income = frame.Close.iloc[-1] / frame.Close.iloc[0] - 1
        strategy_sharpe_ratio = (frame.Strategy_returns.mean() / frame.Strategy_returns.std())*np.sqrt(len(frame))
        asset_sharpe_ratio = (frame.Returns.mean() / frame.Returns.std())*np.sqrt(len(frame))

        ev_message = f"""Доход акции за период составил {round(asset_net_income,2)}\n
Доход стратегии за период составил {round(strategy_net_income,3)}\n
Показатель шарпа акции {round(asset_sharpe_ratio,3)}\n
Показатель шарпа стратегии {round(strategy_sharpe_ratio,3)}\n"""
        
        self.ev_message = ev_message

        


    def __call__(self, indicator):

        local_frame, indicator_data = get_indicator(indicator=indicator, frame=self.frame)
        frame = self.backtest(local_frame)
        self.evaluate(local_frame)

        return self.plot_frame(frame, indicator_data)
