import pandas as pd
import numpy as np

__all__ = ['get_indicator']


class Indicators:

    def moving_average(self, frame, period=24):

        frame['MA24'] = frame.Close.rolling(period).mean()
        frame['Criteria'] = frame.Close > frame.MA24

        return frame


    def ema(self, frame):

        frame['EMA12'] = frame.Close.ewm(span=12).mean()
        # frame['EMA26'] = frame.Close.ewm(span=26).mean()
        frame['Criteria'] = frame['EMA12'] > frame.Close

        return frame


    def bollinger_bands(self, frame):

        raise NotImplementedError
        frame['MA20'] = frame.Close.rolling(20).mean()
        frame['STD20'] = frame.Close.rolling(20).std()
        frame['lower_band'] = frame['MA20'] - frame['STD20'] * 2
        frame['upper_band'] = frame['MA20'] + frame['STD20'] * 2


    def rsi(self, frame):

        raise NotImplementedError


    def cci(self, frame):
        
        raise NotImplementedError


    def stockhastic(self, frame):

        frame['Min'] = frame.Low.rolling(14).min()
        frame['close-min'] = frame.Close - frame.Min
        frame['H-L'] = frame.High.rolling(14).max() - frame.Low.rolling(14).min()
        frame['K'] = frame['close-min'] / frame['H-L'] * 100
        frame['SlowK'] = (frame['close-min'].rolling(3).sum() / frame['H-L'].rolling(3).sum()) * 100
        frame['Criteria'] = np.where((frame.SlowK > 25) & (frame.SlowK < 85), True, False )

        return frame


    def standard_deviation(self, frame, period = 24):
        
        raise NotImplementedError


    def macd(self, frame):

        frame['EMA12'] = frame.Close.ewm(span=12).mean()
        frame['EMA26'] = frame.Close.ewm(span=26).mean()
        frame['Difference'] = frame.EMA12 - frame.EMA26
        frame['Signal'] = frame.Difference.ewm(span=9).mean() #9 period ema
        frame['Histogram'] = frame.Difference - frame.Signal
        frame['Criteria'] = frame.Histogram > 0

        return frame


    def slope(self, frame, period, angle):
        pass


    def get_indicator(self, indicator, frame, **kwargs):
        method = getattr(self, indicator)
        return method(frame, **kwargs)

get_indicator = Indicators().get_indicator
