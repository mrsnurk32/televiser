import pandas as pd

__all__ = ['get_indicator']


class Indicators:

    def moving_average(self, frame, period=24):
        print('MA')
        frame = frame['frame']
        frame['MA24'] = frame.Close.rolling(period).mean()
        frame['Criteria'] = frame.Close > frame.MA24
        return frame


    def ema(self, frame, period=12):
        pass


    def rsi(self, frame):
        pass


    def cci(self, frame):
        pass


    def stockhastic(self, frame):
        pass


    def standard_deviation(self, frame, period = 24):
        pass


    def macd(self, frame):
        pass


    def slope(self, frame, period, angle):
        pass


    def get_indicator(self, indicator, **kwargs):
        method = getattr(self, indicator)
        return method(kwargs)

get_indicator = Indicators().get_indicator
