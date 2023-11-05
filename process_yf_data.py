import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

class ProcessYFData:
    def __init__(self, short_window=20, long_window=50, med_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.med_window = med_window

    def bollinger_bands(self, series, num_std, window=20):
        MA = series.rolling(window=window)
        std = MA.std()
        return MA.mean() + num_std * std, MA.mean() - num_std * std

    def moving_average(self, data: pd.Series, window):
        return data.rolling(window=window, min_periods=window).mean()

    def prep_data(self, df):
        df['TP'] = (df.High +  df.Low +  df.Close) / 3
        df['MA_short'] = self.moving_average(df.Close, self.short_window)
        df['MA_long'] = self.moving_average(df.Close, self.long_window)
        df['SMA'] = self.moving_average(df.TP, self.med_window)
        df['upper_BB'], df['lower_BB'] = self.bollinger_bands(df.TP, 2, window=self.med_window)
        return df

    def visual(self, df, interval: list):
        plt.figure(figsize=(20,10))
        dates = df.index
        plt.plot(dates, df.TP, label='Typical Price')
        plt.plot(dates, df['SMA'], color='black', label='SMA')
        plt.plot(dates, df['upper_BB'], label='UB', color='red', alpha=0.5)
        plt.plot(dates, df['lower_BB'], label='LB', color='green', alpha=0.5)
        plt.fill_between(dates, df['upper_BB'], df['lower_BB'], color='grey', alpha=0.1)
        period = ' to '.join(str(x) for x in interval)
        plt.title(f'Bollinger Bands on Typical Price from {period}', fontsize = 17)
        plt.legend(loc='upper left', fontsize = 17)
        plt.ylabel('Price')
        plt.xlabel('Days')
        plt.show()