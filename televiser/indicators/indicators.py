import pandas as pd
import numpy as np

__all__ = ['get_indicator']


class Indicators:

    def moving_average(self, frame, period=24):

        frame = frame['frame']
        frame['MA24'] = frame.Close.rolling(period).mean()
        frame['Criteria'] = frame.Close > frame.MA24

        indicator_data = {
            'title':"MA",
            'col_1':{
                'plot_type':'line',
                'plot_col':'MA',
            },
        }

        return frame, indicator_data


    def ema(self, frame, period=12):

        frame = frame['frame']
        frame['EMA12'] = frame.Close.ewm(span=12).mean()
        # frame['EMA26'] = frame.Close.ewm(span=26).mean()
        frame['Criteria'] = frame['EMA12'] > frame.Close

        indicator_data = {
            'title':"EMA",
            'col_1':{
                'plot_type':'line',
                'plot_col':'EMA12',
            },
        }

        return frame, indicator_data


    def bollinger_bands(self, frame):

        raise NotImplementedError
        frame = frame['frame']
        frame['MA20'] = frame.Close.rolling(20).mean()
        frame['STD20'] = frame.Close.rolling(20).std()
        frame['lower_band'] = frame['MA20'] - frame['STD20'] * 2
        frame['upper_band'] = frame['MA20'] + frame['STD20'] * 2


    def rsi(self, frame):

        raise NotImplementedError


    def cci(self, frame):
        
        raise NotImplementedError


    def stockhastic(self, frame):

        frame = frame['frame']
        frame['Min'] = frame.Low.rolling(14).min()
        frame['close-min'] = frame.Close - frame.Min
        frame['H-L'] = frame.High.rolling(14).max() - frame.Low.rolling(14).min()
        frame['K'] = frame['close-min'] / frame['H-L'] * 100
        frame['SlowK'] = (frame['close-min'].rolling(3).sum() / frame['H-L'].rolling(3).sum()) * 100
        frame['Criteria'] = np.where((frame.SlowK > 25) & (frame.SlowK < 85), True, False )
        
        indicator_data = {
            'title':"Stockhastic",
            'col_1':{
                'plot_type':'line',
                'plot_col':'SlowK',
            },
        }

        return frame, indicator_data


    def standard_deviation(self, frame, period = 24):
        
        raise NotImplementedError


    def macd(self, frame):

        frame = frame['frame']
        frame['EMA12'] = frame.Close.ewm(span=12).mean()
        frame['EMA26'] = frame.Close.ewm(span=26).mean()
        frame['Difference'] = frame.EMA12 - frame.EMA26
        frame['Signal'] = frame.Difference.ewm(span=9).mean() #9 period ema
        frame['Histogram'] = frame.Difference - frame.Signal
        frame['Criteria'] = frame.Histogram > 0

        indicator_data = {
            'title':"MACD",
            'col_1':{
                'plot_type':'bar',
                'plot_col':'Histogram',
            },
        }

        return frame, indicator_data


    def slope(self, frame, period, angle):
        pass


    def get_indicator(self, indicator, **kwargs):
        method = getattr(self, indicator)
        return method(kwargs)

get_indicator = Indicators().get_indicator
