import pandas as pd
import numpy as np
import math
import json
import datetime
import time
from functools import partial
from typing import Optional, List, Union, Dict
from multiprocessing import Pool
from .base import Factor
from .fund_basic_factors import *
from ...data.manager import DataManager
from ...data.struct import AssetTimeSpan
from ...data.manager.fund_info_filter import fund_info_update, active_fund_info as get_active_fund_info
from ...constant import FundFactorType 

class FundAlive(Factor):

    def __init__(self):
        super().__init__(f_name='FundAlive', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        fund_info = FundInfo().get()
        fund_nav = FundNavDailyModify().get()
        fund_start_date = fund_info.set_index('fund_id').to_dict()['start_date']
        fund_end_date = fund_info.set_index('fund_id').to_dict()['end_date']
        self._factor = pd.DataFrame(1, columns = fund_nav.columns, index=fund_nav.index)
        res = []
        for fund_id in self._factor:
            s_d = fund_start_date[fund_id]
            e_d = fund_end_date[fund_id]
            df_i = self._factor.loc[s_d:e_d][[fund_id]]
            res.append(df_i)
        self._factor = pd.concat(res,axis=1).sort_index()
        self._factor.index.name = 'datetime'

class TradeYear(Factor):

    def __init__(self):
        super().__init__(f_name='TradeYear', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavDailyModify())
        self._deps.add(TradingDay())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        self._factor = self.fund_nav.rolling(window=self.fund_nav.shape[0],min_periods=1).apply(self.rolling_trade_year, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FeeRate(Factor):

    def __init__(self):
        super().__init__(f_name='FeeRate', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(TradingDay())

    def calc(self):
        fund_info = FundInfo().get()
        fee_dic = fund_info[['fund_id','manage_fee','trustee_fee']].set_index('fund_id').fillna(0).sum(axis = 1)
        self._factor = pd.DataFrame(fee_dic, columns=[datetime.date(2005,1,4)]).T
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AlphaBetaDaily3yI(Factor):
    # cost 20-30 mins
    def __init__(self):
        super().__init__(f_name='AlphaBetaDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfoAsset())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())
        self._deps.add(TradingDay())

    def loop_item(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',self.index_id:'benchmark'}).reset_index()
        res = []
        pd.Series(df.index).rolling(
            window=self.time_range, min_periods=self.MIN_TIME_SPAN).apply(
            partial(self.rolling_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{fund_id}', 'beta':f'beta_{fund_id}'})
        return df
    
    def loop_item_update(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',self.index_id:'benchmark'})
        df = df.loc[:self.update_dt].tail(self.time_range).reset_index()
        res = []
        self._rolling_alpha_beta(res, df)
        fund_res = {f'alpha_{fund_id}':res[0]['alpha'],
                    f'beta_{fund_id}':res[0]['beta']}   
        return fund_res

    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        res = []
        for self.index_id, fund_list in self.index_fund.items():  
            _res = [self.loop_item_update(i) for i in fund_list]
            res.extend(_res)
        for _i in res:
            dic.update(_i)
        print(f'finish {dt}')
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        last_date = self._exsited_factor.index[-1]
        td = self.fund_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        print('update_list  ',update_list)
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        # calculate
        result = []
        for self.index_id, fund_list in self.index_fund.items():
            if is_multi_cpu:
                p = Pool()
                res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64)]
                p.close()
                p.join()
                result.extend(res)
            else:
                for fund_id in fund_list:
                    res_i = self.loop_item(fund_id)
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self.data = None

class AlphaDaily3yI(Factor):

    def __init__(self):
        super().__init__(f_name='AlphaDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaBetaDaily3yI())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = AlphaBetaDaily3yI().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class BetaDaily3yI(Factor):

    def __init__(self):
        super().__init__(f_name='BetaDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaBetaDaily3yI())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = AlphaBetaDaily3yI().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AlphaMdd3yI(Factor):

    def __init__(self):
        super().__init__(f_name='AlphaMdd3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaDaily3yI())

    def calc(self):
        self.alpha = AlphaDaily3yI().get()
        self._factor = self.alpha.rolling(window=self.alpha.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_mdd, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class WinRateMonthlyI(Factor):
        
    def __init__(self):
        super().__init__(f_name='WinRateMonthlyI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(ActiveFundInfo())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())
        self._deps.add(FundInfoAsset())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)
        
        self.fund_ret_monthly = self.data_resample_monthly_ret(self.fund_ret).dropna(axis=0,how='all')
        self.index_ret_monthly = self.data_resample_monthly_ret(self.index_ret).dropna(axis=0,how='all')
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            con_df = ~ self.fund_ret_monthly[fund_list].isnull() * 1
            con_df = con_df.replace(0,np.nan)
            winrate = self.fund_ret_monthly[fund_list].gt(self.index_ret_monthly[self.index_id],axis='index') * 1
            res_i = (con_df * winrate).rolling(window=winrate.shape[0],min_periods=6).mean()
            res.append(res_i)
        self._factor = pd.concat(res, axis=1)

class WinRateMonthlyTop50(Factor):

    def __init__(self):
        super().__init__(f_name='WinRateMonthlyTop50', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(ActiveFundInfo())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())
        self._deps.add(FundInfoAsset())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        self.fund_ret_monthly = self.data_resample_monthly_ret(self.fund_ret).dropna(axis=0,how='all')
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)
        top_pct = 0.5
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            _df = self.fund_ret_monthly[fund_list]
            con_df = ~ _df.isnull() * 1
            con_df = con_df.replace(0,np.nan)
            _df_rank = _df.rank(pct=True,axis=1).copy()
            top_df = (_df_rank > top_pct) * 1
            res_i = (con_df * top_df).rolling(window=top_df.shape[0],min_periods=6).mean()
            res.append(res_i)
        self._factor = pd.concat(res, axis=1)

class WinRateMonthlyTop75(Factor):

    def __init__(self):
        super().__init__(f_name='WinRateMonthlyTop75', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(ActiveFundInfo())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())
        self._deps.add(FundInfoAsset())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        self.fund_ret_monthly = self.data_resample_monthly_ret(self.fund_ret).dropna(axis=0,how='all')
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)
        
        top_pct = 0.75
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            _df = self.fund_ret_monthly[fund_list]
            con_df = ~ _df.isnull() * 1
            con_df = con_df.replace(0,np.nan)
            _df_rank = _df.rank(pct=True,axis=1).copy()
            top_df = (_df_rank > top_pct) * 1
            res_i = (con_df * top_df).rolling(window=top_df.shape[0],min_periods=6).mean()
            res.append(res_i)
        self._factor = pd.concat(res, axis=1)

class TrackerrDaily3yI(Factor):

    def __init__(self):
        super().__init__(f_name='TrackerrDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(ActiveFundInfo())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())
        self._deps.add(TradingDay())
        self._deps.add(FundInfoAsset())

    def loop_item(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df['track_err'] = (df[fund_id] - df[self.index_id]).rolling(window=self.time_range, min_periods=self.MIN_TIME_SPAN).std(ddof=1)* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        df = df[['track_err']].rename(columns={'track_err': fund_id})
        return df

    def loop_item_update(self, fund_id):
        df = self.data.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        track_err = (df[fund_id] - df[self.index_id]).loc[:self.update_dt].tail(self.time_range).std(ddof=1)* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        return {'fund_id':fund_id, 'track_err':track_err}

    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            _res = [self.loop_item_update(i) for i in fund_list]
            res.extend(_res)
        _df = pd.DataFrame(res).set_index('fund_id').T
        _df.index = [self.update_dt]
        return _df
    
    def append_update(self):
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        last_date = self._exsited_factor.index[-1]
        td = self.fund_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        
        # calculate
        result = []
        for self.index_id, fund_list in self.index_fund.items():
            if is_multi_cpu:
                p = Pool()
                res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64)]
                p.close()
                p.join()
                result.extend(res)
            else:
                for fund_id in fund_list:
                    res_i = self.loop_item(fund_id)
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        
class InfoRatioDaily3yI(Factor):

    def __init__(self):
        super().__init__(f_name='InfoRatioDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaDaily3yI())
        self._deps.add(TrackerrDaily3yI())
        self._deps.add(TradingDay())

    def calc(self):
        alpha = AlphaDaily3yI().get()
        track_err = TrackerrDaily3yI().get()
        common_funds = alpha.columns.intersection(track_err.columns)
        self._factor = alpha[common_funds] / track_err[common_funds]
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MddDaily3y(Factor):

    def __init__(self):
        super().__init__(f_name='MddDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavDailyModify())
        self._deps.add(TradingDay())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_mdd, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class TreynorDaily3yI(Factor):

    def __init__(self):
        super().__init__(f_name='TreynorDaily3yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(BetaDaily3yI())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        beta = BetaDaily3yI().get()
        self.fund_ret = FundRetDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        common_funds = beta.columns.intersection(self.fund_ret.columns)
        fund_mean_ret = self.fund_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).mean()
        fund_mean_ret_no_free_ret = fund_mean_ret - self.RISK_FEE_RATE_PER_DAY
        self._factor = fund_mean_ret_no_free_ret[common_funds] * self.TRADING_DAYS_PER_YEAR / beta[common_funds]
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class DownriskDaily3y(Factor):

    def __init__(self):
        super().__init__(f_name='DownriskDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        down_ret = np.abs(np.minimum(self.fund_ret - self.RISK_FEE_RATE_PER_DAY, 0))
        self._factor = down_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).mean()* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class RetOverPeriodDaily3y(Factor):
    
    def __init__(self):
        super().__init__(f_name='RetOverPeriodDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav / self.fund_nav.fillna(method='bfill').shift(self.time_range) - 1
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualRetDaily3y(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualRetDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualVolDaily3y(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualVolDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        year = 3
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class SharpeDaily3y(Factor):

    def __init__(self):
        super().__init__(f_name='SharpeDaily3y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AnnualRetDaily3y())
        self._deps.add(AnnualVolDaily3y())
        self._deps.add(TradingDay())

    def calc(self):
        annual_ret = AnnualRetDaily3y().get()
        annual_vol = AnnualVolDaily3y().get()
        self._factor =  (annual_ret - self.RISK_FEE_RATE) / annual_vol
        self._factor = self._factor.replace(-np.Inf,np.nan).replace(np.Inf,np.nan)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AlphaBetaDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='AlphaBetaDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfoAsset())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())

    def loop_item(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',self.index_id:'benchmark'}).reset_index()
        res = []
        pd.Series(df.index).rolling(
            window=self.time_range, min_periods=self.MIN_TIME_SPAN).apply(
            partial(self.rolling_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{fund_id}', 'beta':f'beta_{fund_id}'})
        return df
    
    def loop_item_update(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',self.index_id:'benchmark'})
        df = df.loc[:self.update_dt].tail(self.time_range).reset_index()
        res = []
        self._rolling_alpha_beta(res, df)
        fund_res = {f'alpha_{fund_id}':res[0]['alpha'],
                    f'beta_{fund_id}':res[0]['beta']}   
        return fund_res

    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            _res = [self.loop_item_update(i) for i in fund_list]
            res.extend(_res)
        for _i in res:
            dic.update(_i)
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        last_date = self._exsited_factor.index[-1]
        td = self.fund_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        # calculate
        result = []
        for self.index_id, fund_list in self.index_fund.items():
            if is_multi_cpu:
                p = Pool()
                res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64)]
                p.close()
                p.join()
                result.extend(res)
            else:
                for fund_id in fund_list:
                    res_i = self.loop_item(fund_id)
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        
class AlphaDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='AlphaDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaBetaDaily1yI())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = AlphaBetaDaily1yI().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class BetaDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='BetaDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaBetaDaily1yI())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = AlphaBetaDaily1yI().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class TrackerrDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='TrackerrDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfoAsset())
        self._deps.add(FundRetDailyModify())
        self._deps.add(IndexRetDaily())

    def loop_item(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        df['track_err'] = (df[fund_id] - df[self.index_id]).rolling(window=self.time_range, min_periods=self.MIN_TIME_SPAN).std(ddof=1)* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        df = df[['track_err']].rename(columns={'track_err': fund_id})
        return df

    def loop_item_update(self, fund_id):
        df = self.fund_ret[[fund_id]].join(self.index_ret[[self.index_id]]).dropna()
        track_err = (df[fund_id] - df[self.index_id]).loc[:self.update_dt].tail(self.time_range).std(ddof=1)* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        return {'fund_id':fund_id, 'track_err':track_err}

    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        res = []
        for self.index_id, fund_list in self.index_fund.items():
            _res = [self.loop_item_update(i) for i in fund_list]
            res.extend(_res)
        _df = pd.DataFrame(res).set_index('fund_id').T
        _df.index = [self.update_dt]
        return _df
    
    def append_update(self):
        self._exsited_factor = self.get()
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)

        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        last_date = self._exsited_factor.index[-1]
        td = self.fund_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self.fund_ret = FundRetDailyModify().get()
        self.index_ret = IndexRetDaily().get()
        fund_info_asset = FundInfoAsset().get()
        fund_info_asset = fund_info_asset[['fund_id','bk_index_id']].dropna()
        self.index_fund = {}
        for r in fund_info_asset.itertuples():
            if r.bk_index_id not in self.index_fund:
                self.index_fund[r.bk_index_id] = []
            self.index_fund[r.bk_index_id].append(r.fund_id)
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        
        # calculate
        result = []
        for self.index_id, fund_list in self.index_fund.items():
            if is_multi_cpu:
                p = Pool()
                res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64)]
                p.close()
                p.join()
                result.extend(res)
            else:
                for fund_id in fund_list:
                    res_i = self.loop_item(fund_id)
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class InfoRatioDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='InfoRatioDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AlphaDaily1yI())
        self._deps.add(TrackerrDaily1yI())
        self._deps.add(TradingDay())

    def calc(self):
        alpha = AlphaDaily1yI().get()
        track_err = TrackerrDaily1yI().get()
        common_funds = alpha.columns.intersection(track_err.columns)
        self._factor = alpha[common_funds] / track_err[common_funds]
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MddDaily1y(Factor):

    def __init__(self):
        super().__init__(f_name='MddDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_mdd, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class TreynorDaily1yI(Factor):

    def __init__(self):
        super().__init__(f_name='TreynorDaily1yI', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())
        self._deps.add(BetaDaily3yI())

    def calc(self):
        beta = BetaDaily3yI().get()
        self.fund_ret = FundRetDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        common_funds = beta.columns.intersection(self.fund_ret.columns)
        fund_mean_ret = self.fund_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).mean()
        fund_mean_ret_no_free_ret = fund_mean_ret - self.RISK_FEE_RATE_PER_DAY
        self._factor = fund_mean_ret_no_free_ret[common_funds] * self.TRADING_DAYS_PER_YEAR / beta[common_funds]
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class DownriskDaily1y(Factor):

    def __init__(self):
        super().__init__(f_name='DownriskDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        down_ret = np.abs(np.minimum(self.fund_ret - self.RISK_FEE_RATE_PER_DAY, 0))
        self._factor = down_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).mean()* np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class RetOverPeriodDaily1y(Factor):
    
    def __init__(self):
        super().__init__(f_name='RetOverPeriodDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav / self.fund_nav.fillna(method='bfill').shift(self.time_range) - 1
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualRetDaily1y(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualRetDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav =  FundNavDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_nav.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualVolDaily1y(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualVolDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        year = 1
        self.time_range = year * self.TRADING_DAYS_PER_YEAR
        self._factor = self.fund_ret.rolling(window=self.time_range,min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class SharpeDaily1y(Factor):

    def __init__(self):
        super().__init__(f_name='SharpeDaily1y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AnnualRetDaily1y())
        self._deps.add(AnnualVolDaily1y())
        self._deps.add(TradingDay())

    def calc(self):
        annual_ret = AnnualRetDaily1y().get()
        annual_vol = AnnualVolDaily1y().get()
        self._factor =  (annual_ret - self.RISK_FEE_RATE) / annual_vol
        self._factor = self._factor.replace(-np.Inf,np.nan).replace(np.Inf,np.nan)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualRetDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualRetDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundNavDailyModify())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        self._factor = self.fund_nav.rolling(window=self.fund_nav.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualVolDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='AnnualVolDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self.fund_ret = FundRetDailyModify().get()
        self._factor = self.fund_ret.rolling(window=self.fund_ret.shape[0],min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class AnnualRetMonthlyHalfY(Factor):
    # 不在日度做reindex 算ContinueRegValue用
    def __init__(self):
        super().__init__(f_name='AnnualRetMonthlyHalfY', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavMonthlyModify())

    def calc(self):
        self.fund_nav = FundNavMonthlyModify().get()
        self._factor = self.fund_nav.rolling(window=6).apply(self.rolling_monthly_annual_ret, raw=True)
        self._factor = self._factor.dropna(axis=0, how='all')

class AnnualVolMonthlyHalfY(Factor):
    # 不在日度做reindex 算ContinueRegValue用
    def __init__(self):
        super().__init__(f_name='AnnualVolMonthlyHalfY', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundRetMonthlyModify())

    def calc(self):
        self.fund_ret = FundRetMonthlyModify().get()
        self._factor = self.fund_ret.rolling(window=6).std(ddof=1) * np.sqrt(12)
        self._factor = self._factor.dropna(axis=0, how='all')

class SharpeMonthlyHalfY(Factor):
    # 不在日度做reindex 算ContinueRegValue用
    def __init__(self):
        super().__init__(f_name='SharpeMonthlyHalfY', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(AnnualRetMonthlyHalfY())
        self._deps.add(AnnualVolMonthlyHalfY())

    def calc(self):
        annual_ret = AnnualRetMonthlyHalfY().get()
        annual_vol = AnnualVolMonthlyHalfY().get()
        self._factor =  (annual_ret - self.RISK_FEE_RATE) / annual_vol
        self._factor = self._factor.replace(-np.Inf,np.nan).replace(np.Inf,np.nan)
        self._factor = self._factor.dropna(axis=0, how='all')

class ContinueRegValue(Factor):

    def __init__(self):
        super().__init__(f_name='ContinueRegValue', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(SharpeMonthlyHalfY())
        self._deps.add(TradingDay())

    def calc(self):
        sharpe = SharpeMonthlyHalfY().get()
        self._factor = sharpe.rolling(window=sharpe.shape[0],min_periods=6).apply(self.rolling_auto_reg, raw=True)
        self._factor = self._factor.dropna(axis=0, how='all')
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class TotalRetDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='TotalRetDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavDailyModify())
        self._deps.add(TradingDay())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        self._factor = self.fund_nav.rolling(window=self.fund_nav.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_totol_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MddDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MddDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavDailyModify())
        self._deps.add(TradingDay())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get() 
        self._factor = self.fund_nav.rolling(window=self.fund_nav.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_mdd, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class RecentMonthRet(Factor):
    
    def __init__(self):
        super().__init__(f_name='RecentMonthRet', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundNavDailyModify())
        self._deps.add(TradingDay())

    def calc(self):
        self.fund_nav = FundNavDailyModify().get()
        self._factor = self.fund_nav.rolling(window=20,min_periods=5).apply(self.rolling_totol_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class DownsideStdDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='DownsideStdDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundRetDailyModify())

    def calc(self):
        self._factor = FundRetDailyModify().get()
        self._factor[self._factor > 0] = 0
        self._factor = self._factor.rolling(window=self._factor.shape[0],min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClAlphaBetaHistoryWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClAlphaBetaHistoryWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(FundRetWeeklyModify())
        self._deps.add(IndexRetWeekly())
        self._deps.add(TradingDay())
        self._deps.add(FundInfoAsset())

    def loop_item(self, fund_id):
        index_id = self.WIND_TYPE_DICT[self.fund_wind_class_dic[fund_id]]
        df = self.fund_weekly_ret[[fund_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',index_id:'benchmark'}).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        pd.Series(df.index).rolling(
            window=df.shape[0], min_periods=24).apply(
            partial(self.rolling_cl_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{fund_id}', 'beta':f'beta_{fund_id}'})
        return df

    def loop_item_update(self, fund_id):
        index_id = self.WIND_TYPE_DICT[self.fund_wind_class_dic[fund_id]]
        df = self.fund_weekly_ret[[fund_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',index_id:'benchmark'}).loc[:self.update_dt].reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        self._rolling_cl_alpha_beta(res, df[['fund','benchmark']].to_numpy())
        fund_res = {f'alpha_{fund_id}':res[0]['alpha'],
                    f'beta_{fund_id}':res[0]['beta']}   
        return fund_res
    
    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        fund_list = self.fund_weekly_ret.columns.tolist()
        result = [self.loop_item_update(i) for i in fund_list]
        for _i in result:
            if _i is not None:
                dic.update(_i)
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self.fund_info = FundInfo().get()
        self.fund_weekly_ret = FundRetWeeklyModify().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        self.fund_wind_class_dic = self.fund_info.set_index('fund_id').to_dict()['wind_class_2']
        
        last_date = self._exsited_factor.index[-1]
        td = self.fund_weekly_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self.fund_info = FundInfo().get()
        self.fund_weekly_ret = FundRetWeeklyModify().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        self.fund_wind_class_dic = self.fund_info.set_index('fund_id').to_dict()['wind_class_2']
        
        fund_list = self.fund_weekly_ret.columns.tolist()
        # calculate
        result = []
        if is_multi_cpu:
            p = Pool()
            res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64) if i is not None]
            p.close()
            p.join()
            result.extend(res)
        else:
            for fund_id in fund_list:
                res_i = self.loop_item(fund_id)
                if res_i is not None:
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor.index.name = 'datetime'
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClAlphaHistoryWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClAlphaHistoryWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundClAlphaBetaHistoryWeekly())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = FundClAlphaBetaHistoryWeekly().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClBetaHistoryWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClBetaHistoryWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundClAlphaBetaHistoryWeekly())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = FundClAlphaBetaHistoryWeekly().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClAlphaBeta1YWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClAlphaBeta1YWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundInfo())
        self._deps.add(FundRetWeeklyModify())
        self._deps.add(IndexRetWeekly())
        self._deps.add(TradingDay())

    def loop_item(self, fund_id):
        index_id = self.WIND_TYPE_DICT[self.fund_wind_class_dic[fund_id]]
        df = self.fund_weekly_ret[[fund_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',index_id:'benchmark'}).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        pd.Series(df.index).rolling(
            window=52, min_periods=24).apply(
            partial(self.rolling_cl_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{fund_id}', 'beta':f'beta_{fund_id}'})
        return df
    
    def loop_item_update(self, fund_id):
        index_id = self.WIND_TYPE_DICT[self.fund_wind_class_dic[fund_id]]
        df = self.fund_weekly_ret[[fund_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={fund_id:'fund',index_id:'benchmark'}).loc[:self.update_dt].tail(52).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        self._rolling_cl_alpha_beta(res, df[['fund','benchmark']].to_numpy())
        fund_res = {f'alpha_{fund_id}':res[0]['alpha'],
                    f'beta_{fund_id}':res[0]['beta']}   
        return fund_res
    
    def update_one_day(self, dt):
        self.update_dt = dt
        dic = {}
        fund_list = self.fund_weekly_ret.columns.tolist()
        res = [self.loop_item_update(i) for i in fund_list]
        for _i in res:
            if _i is not None:
                dic.update(_i)
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self.fund_info = FundInfo().get()
        self.fund_weekly_ret = FundRetWeeklyModify().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        self.fund_wind_class_dic = self.fund_info.set_index('fund_id').to_dict()['wind_class_2']
        last_date = self._exsited_factor.index[-1]
        td = self.fund_weekly_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self.fund_info = FundInfo().get()
        self.fund_weekly_ret = FundRetWeeklyModify().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        self.fund_wind_class_dic = self.fund_info.set_index('fund_id').to_dict()['wind_class_2']
        fund_list = self.fund_weekly_ret.columns.tolist()
        # calculate
        result = []
        if is_multi_cpu:
            p = Pool()
            res = [i for i in p.imap_unordered(self.loop_item, fund_list, 64) if i is not None]
            p.close()
            p.join()
            result.extend(res)
        else:
            for fund_id in fund_list:
                res_i = self.loop_item(fund_id)
                if res_i is not None:
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor.index.name = 'datetime'
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClAlpha1YWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClAlpha1YWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundClAlphaBeta1YWeekly())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = FundClAlphaBeta1YWeekly().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class FundClBeta1YWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='FundClBeta1YWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(FundClAlphaBetaHistoryWeekly())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = FundClAlphaBetaHistoryWeekly().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.split('_')[1] for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class ManagerIndex(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndex', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(IndexCloseDaily())
        self._deps.add(FundInfo())
        self._deps.add(FundManagerInfo())
        self._deps.add(FundSizeCombine())
        self._deps.add(FundNavDailyModify())
        self._deps.add(FundRetDailyModify())

    def fund_manager_prepare(self, start_date=None):
        self.mng_index_list: Dict[str, pd.DataFrame] = {}  # 基金经理指数
        self.mng_best_fund: Dict[str, pd.DataFrame] = {}  # 基金经理代表作 
        self.trading_days_list = TradingDay().get().index
        self.full_trading_days_list = DataManager.basic_data(func_name='get_trading_day_list').datetime
        self.full_trading_days_list = self.full_trading_days_list[self.full_trading_days_list >= datetime.date(2004,12,1)]
        self.index_price = IndexCloseDaily().get().rename(columns=self.INDEX_DICT)
        self.index_ret = np.log(self.index_price).diff()
        self.fund_info = FundInfo().get()
        self.fund_manager_info = FundManagerInfo().get()
        self.fund_manager_info = self.fund_manager_info.rename(columns={'mng_id': 'manager_id', 'mng_name': 'name', 'start_date': 'start', 'end_date': 'end'})
        ## 计算基金经理指数时只去掉分级基金子基金， 不能回测交易的基金依然影响基金经理能力
        self.fund_info = self.fund_info[(self.fund_info.structure_type <= 1)
                                        & (~self.fund_info.wind_class_2.isnull())]
        self.fund_size = FundSizeCombine().get()
        self.fund_nav = FundNavDailyModify().get()
        self.fund_ret = FundRetDailyModify().get()
        if start_date is not None:
            self.index_price = self.index_price.loc[start_date:]
            self.index_ret = self.index_ret.loc[start_date:]
            self.fund_info = self.fund_info[self.fund_info.end_date >= start_date]
            self.fund_manager_info = self.fund_manager_info[self.fund_manager_info.end >= start_date]
            self.fund_size = self.fund_size.loc[start_date:]
            self.fund_nav = self.fund_nav.loc[start_date:]
            self.fund_ret = self.fund_ret.loc[start_date:]
            self.full_trading_days_list = self.full_trading_days_list[self.full_trading_days_list > (start_date - datetime.timedelta(days=5))]
        self.manager_name_dict = self.fund_manager_info.set_index('manager_id').to_dict()['name'] 
        self.fund_manager_info = self.fund_manager_info.set_index('fund_id')
        # 每个基金经理人数   如果多人给惩罚
        fund_list = self.fund_manager_info.index.unique().tolist()
        self.fund_manager_num_df = self.mng_process_manager_num(fund_list, self.fund_ret.index)
        
        # 每个基金的规模  小于1e 给惩罚
        self.fund_manager_size_df = self.fund_size.copy()
        self.fund_manager_size_df[self.fund_manager_size_df < 1e8] = 0.6
        self.fund_manager_size_df[(self.fund_manager_size_df >= 1e8) & (self.fund_manager_size_df < 2e9)] = 0.7
        self.fund_manager_size_df[(self.fund_manager_size_df >= 2e9) & (self.fund_manager_size_df < 5e9)] = 0.8
        self.fund_manager_size_df[(self.fund_manager_size_df >= 5e9) & (self.fund_manager_size_df < 1e10)] = 0.9
        self.fund_manager_size_df[self.fund_manager_size_df >= 1e10] = 1
        self.fund_manager_size_df = self.fund_manager_size_df.fillna(self.PUNISH_RATIO)

        # 基金经理数据 根据被动主动分类
        pass_fund_id_list = self.fund_info[self.fund_info.wind_class_2.str.contains('被动')].fund_id.tolist()
        pass_fund_id_list = [i for i in pass_fund_id_list if i in self.fund_ret.columns] 
        acti_fund_id_list = [i for i in self.fund_ret.columns if i not in pass_fund_id_list] 
        _df_acti = pd.DataFrame(1, columns=acti_fund_id_list, index=self.fund_ret.index)
        _df_pass = pd.DataFrame(self.PUNISH_RATIO, columns=pass_fund_id_list, index=self.fund_ret.index)
        self.fund_manager_stype_df = pd.concat([_df_acti, _df_pass], axis=1)
        
        for fund_type in self.FUND_CLASSIFIER:
            self.mng_index_list[fund_type] = pd.DataFrame(index=self.fund_ret.index)
            self.mng_best_fund[fund_type] = pd.DataFrame(index=self.fund_ret.index)

    def mng_lambda_filter_date_range(self, single_fund_info: pd.DataFrame, date_index: pd.Series) -> pd.Series:
        result: List[pd.Series] = []
        for row in single_fund_info.itertuples(index=False):
            result.append(pd.Series((date_index >= row.start) & (date_index <= row.end), index=date_index))
        return pd.concat(result, axis=1).sum(axis=1)

    def mng_process_fund_ret(self, this_manager_fund_ids, this_manager_info, date_index):
        res = []
        for fund_id in this_manager_fund_ids:
            single_fund_info = this_manager_info.loc[[fund_id]]
            res_i =  self.mng_lambda_filter_date_range(single_fund_info, date_index)
            res_i.name = fund_id
            res.append(res_i)
        return pd.concat(res, axis=1)

    def mng_process_manager_num(self, fund_id_list, date_index):
        res = []
        for fund_id in fund_id_list:
            fund_managers_info = self.fund_manager_info.loc[[fund_id]]
            fund_manager_list = fund_managers_info.manager_id.unique()
            _res = []
            for _mng_id in fund_manager_list:
                fund_manager_i = fund_managers_info[fund_managers_info['manager_id'] == _mng_id]
                single_fund_res = self.mng_lambda_filter_date_range(fund_manager_i, date_index)
                single_fund_res = pd.DataFrame(single_fund_res, columns=[_mng_id])
                _res.append(single_fund_res)
            manager_in_same_time = pd.concat(_res,axis=1)
            fund_manger_same_time = pd.DataFrame(manager_in_same_time.sum(axis=1), columns=[fund_id])            
            res.append(fund_manger_same_time)
        fund_manger_same_time = pd.concat(res, axis=1)
        fund_manger_same_time[fund_manger_same_time > 1] = self.PUNISH_RATIO
        return fund_manger_same_time

    def mng_process_manager_experience(self, fund_id_list, this_manager_info, date_index):
        res = []
        for fund_id in fund_id_list:
            single_fund_info = this_manager_info.loc[[fund_id]]
            work_day_df_i = self.mng_lambda_filter_date_range(single_fund_info, date_index)
            work_day_df_i.name = fund_id
            res.append(work_day_df_i)
        work_day_df = pd.DataFrame(res).T
        work_day_df = work_day_df.cumsum()
        low_cons = work_day_df < self.TRADING_DAYS_PER_YEAR
        mid_cons = (work_day_df >= self.TRADING_DAYS_PER_YEAR) & (work_day_df < 3 * self.TRADING_DAYS_PER_YEAR)
        hig_cons = work_day_df >= 3 * self.TRADING_DAYS_PER_YEAR
        work_day_df[low_cons] = self.HARD_PUNISH_RATIO
        work_day_df[mid_cons] = self.PUNISH_RATIO
        work_day_df[hig_cons] = 1
        return work_day_df

    def calc(self):
        self.fund_manager_prepare()
        fund_manager_list = list(self.manager_name_dict.keys())
        t0 = time.time()
        for m_id in fund_manager_list:
            _t0 = time.time()
            for fund_type in self.FUND_CLASSIFIER:
                idx = self.index_calculation(m_id, fund_type, None)
                if idx is not None:
                    self.mng_index_list[fund_type].loc[:, m_id] = idx # 该资产类别下记录计算结果
            _idx = fund_manager_list.index(m_id)
            _t1 = time.time()
            #print(f'm_id {m_id} {_idx} {len(fund_manager_list)} cost time {_t1 - _t0}')
        t1 = time.time()
        #print(f'total cost {t1 - t0}')
        for fund_type in self.FUND_CLASSIFIER:
            self.mng_index_list[fund_type] = self.mng_index_list[fund_type].replace(0, np.nan).dropna(how='all')
    
        res = []
        for fund_type, mng_index in self.mng_index_list.items():
            df = mng_index.copy()
            df.columns = [fund_type + '_' + i for i in df.columns]
            res.append(df)
        self.mng_index = pd.concat(res,axis=1).dropna(axis=1,how='all')
          
        res = []
        for fund_type, mng_index in self.mng_best_fund.items():
            df = mng_index.copy()
            print(fund_type)
            df.columns = ['bf_' + fund_type + '_' + i for i in df.columns] 
            res.append(df)
        self.mng_best_fund = pd.concat(res,axis=1).dropna(axis=1,how='all')
        # self.s3_uri = 's3://tl-fund-factors/derived/ManagerBestFund.parquet'
        # self.save()
        
    def loop_item(self, m_id):
        _t0 = time.time()
        res = {'mng_id': m_id}
        for fund_type in self.FUND_CLASSIFIER:
            idx = self.index_calculation(m_id, fund_type, self.update_dt)
            if idx is not None:
                res['fund_type'] = idx
        _t1 = time.time()
        print(f'm_id {m_id} cost time {_t1 - _t0}')
        return res

    def append_update(self):
        self._exsited_factor = self.get()
        mng_index_uri = self._get_s3_factor_uri
        mng_best_fund_uri = mng_index_uri.replace('ManagerIndex','ManagerBestFund')
        self._exstied_mng_best_fund = pd.read_parquet(mng_best_fund_uri)
        
        self.update_dt = self._exsited_factor.index[-1]
        self.fund_manager_prepare(self.update_dt)
        fund_manager_list = list(self.manager_name_dict.keys())
        
        t0 = time.time()
        for m_id in fund_manager_list:
            _t0 = time.time()
            for fund_type in self.FUND_CLASSIFIER:
                idx = self.index_calculation(m_id, fund_type, self.update_dt )
                if idx is not None:
                    self.mng_index_list[fund_type].loc[:, m_id] = idx # 该资产类别下记录计算结果
            _idx = fund_manager_list.index(m_id)
            _t1 = time.time()
            #print(f'm_id {m_id} {_idx} {len(fund_manager_list)} cost time {_t1 - _t0}')
        t1 = time.time()
        print(f'total cost time {t1 - t0}')

        res_df = []
        for fund_type, mng_index in self.mng_index_list.items():
            df = mng_index.copy()
            df.columns = [f'{fund_type}_{i}' for i in df.columns]
            df = df / df.iloc[0]
            df_part = (self._exsited_factor[df.columns].iloc[-1] * df).iloc[1:]
            res_df.append(df_part)
        update_result = pd.concat(res_df,axis=1)
        self.mng_index = self._exsited_factor.append(update_result)

        mng_best_fund_uri = mng_index_uri.replace('ManagerIndex','ManagerBestFund')
        self._exstied_mng_best_fund = pd.read_parquet(mng_best_fund_uri)
        _res_best_fund = []
        for fund_type, best_df in self.mng_best_fund.items():
            df = best_df.copy()
            df.columns = [f'bf_{fund_type}_{i}' for i in df.columns]
            _res_best_fund.append(df.iloc[1:])
        self.mng_best_fund = self._exstied_mng_best_fund.append(pd.concat(_res_best_fund,axis=1))
        return self.save()

    def save(self):
        try:
            mng_index_uri = self._get_s3_factor_uri
            self.mng_index.to_parquet(mng_index_uri, compression='gzip')
            print(f' upload to s3 success {mng_index_uri}')

            mng_best_fund_uri = mng_index_uri.replace('ManagerIndex','ManagerBestFund')
            self.mng_best_fund.to_parquet(mng_best_fund_uri, compression='gzip')
            print(f' upload to s3 success {mng_best_fund_uri}')
            self.data = None
            return True
        except:
            return False

    def index_calculation(self, m_id: str, fund_type: str, update_date: None):
        wind_class_2_list = self.FUND_CLASSIFIER[fund_type]
        # 该基金经理管理基金信息
        this_manager_info = self.fund_manager_info[(self.fund_manager_info['wind_class_2'].isin(wind_class_2_list))
                            & (self.fund_manager_info['manager_id'] == m_id)]
        if this_manager_info.shape[0] == 0:
            return 
        index_start_date = this_manager_info.start.min()
        if update_date is not None:
            index_start_date = max(update_date, index_start_date)
        index_end_date = this_manager_info.end.max()
        # 该基金经理管理的同类基金列表
        this_manager_fund_ids = this_manager_info.index.unique().tolist()
        _fund_id_list1 = self.fund_ret.columns.tolist()
        _fund_id_list2 = self.fund_manager_size_df.columns.tolist()
        this_manager_fund_ids = list(set(this_manager_fund_ids).intersection(_fund_id_list1).intersection(_fund_id_list2))
        if len(this_manager_fund_ids) == 0:
            return
        fund_ret = self.fund_ret.loc[index_start_date:index_end_date, this_manager_fund_ids]
        # 非管理时间，基金收益赋值0
        manager_status = self.mng_process_fund_ret(this_manager_fund_ids, this_manager_info, fund_ret.index)
        fund_ret = fund_ret * manager_status
        # 基金经理管理的基金 人数状态 单人为 1 ，多人为0.8
        manager_num = self.fund_manager_num_df.loc[index_start_date:index_end_date, this_manager_fund_ids]
        # 基金经理管理的基金 规模状态  > 100e : 1, > 50e : 0.9, > 20e : 0.8, > 1e : 0.7, < 1e : 0.6
        manager_size = self.fund_manager_size_df.loc[index_start_date:index_end_date, this_manager_fund_ids]
        # 基金经理管理的基金 负责年限 大于3 1， 大于1 0.8， 小于1 0.6
        manager_year = self.mng_process_manager_experience(this_manager_fund_ids, this_manager_info, fund_ret.index)
        # 基金经理管理的基金 主动 1 , 被动 0.8
        manager_style = self.fund_manager_stype_df.loc[index_start_date:index_end_date, this_manager_fund_ids]
        # 权重累乘
        fund_weight = manager_num * manager_size * manager_year * manager_style * manager_status
        # 权重和归1
        fund_weight['sum'] = fund_weight.sum(axis=1).T
        fund_weight = fund_weight[this_manager_fund_ids].divide(fund_weight['sum'], axis=0)
        # 基金经理 收益
        total_ret = (fund_ret * fund_weight).sum(axis=1)
        total_ret.name = m_id
        total_ret = pd.DataFrame(total_ret)
        if total_ret.shape[0] == 0:
            return 
        # 基金经理 收益 用指数填充待业期
        index_date_list = manager_status.index[manager_status.sum(axis=1) < 1]
        total_ret.loc[index_date_list, m_id] = self.index_ret.loc[index_date_list, fund_type]
        # 收益初值赋0
        last_trading_day = self.full_trading_days_list[self.full_trading_days_list < total_ret.index.values[0]].values[-1]
        total_ret.loc[last_trading_day] = 0
        total_ret = total_ret.sort_index()
        # 做指数
        fund_manager_index = np.exp(total_ret.cumsum())
        # 基金经理代表作
        manager_best_fund = pd.DataFrame((fund_weight + manager_status.cumsum()/1e8).idxmax(axis=1), columns=[m_id])
        self.mng_best_fund[fund_type].loc[:, m_id] = manager_best_fund
        return fund_manager_index

class ManagerBestFund(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerBestFund', f_type=FundFactorType.DERIVED, f_level='derived')

    def calc(self):
        pass
    
    def save(self):
        return True
    
class ManagerIndexRetDaily(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndexRetDaily', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(ManagerIndex())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = np.log(mng_index).diff(1)
        self._factor = self.data_reindex_daily_trading_day_not_fill(self._factor, TradingDay().get())

class ManagerIndexWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndexWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = self.data_resample_weekly_nav(mng_index).dropna(axis=0, how='all')

class ManagerIndexRetWeekly(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndexWeekly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexWeekly())

    def calc(self):
        mng_index = ManagerIndexWeekly().get()
        self._factor = np.log(mng_index).diff(1)

class ManagerIndexMonthly(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndexMonthly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = self.data_resample_monthly_nav(mng_index).dropna(axis=0, how='all')

class ManagerIndexRetMonthly(Factor):

    def __init__(self):
        super().__init__(f_name='ManagerIndexRetMonthly', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexMonthly())

    def calc(self):
        mng_index = ManagerIndexMonthly().get()
        self._factor = np.log(mng_index).diff(1)

class MngAnnualRetDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngAnnualRetDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=mng_index.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngAnnualRetDaily1Y(Factor):

    def __init__(self):
        super().__init__(f_name='MngAnnualRetDaily1Y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=self.TRADING_DAYS_PER_YEAR,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngAnnualRetDaily3Y(Factor):

    def __init__(self):
        super().__init__(f_name='MngAnnualRetDaily3Y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=self.TRADING_DAYS_PER_YEAR*3,min_periods=self.MIN_TIME_SPAN).apply(self.rolling_annual_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())


class MngTotalRetDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngTotalRetDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=mng_index.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_totol_ret, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngMddDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngMddDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=mng_index.shape[0],min_periods=self.MIN_TIME_SPAN).apply(self.rolling_mdd, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngAnnualVolDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngAnnualVolDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexRetDaily())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index_ret = ManagerIndexRetDaily().get()
        self._factor = mng_index_ret.rolling(window=mng_index_ret.shape[0],min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngDownsideStdDailyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngDownsideStdDailyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexRetDaily())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index_ret = ManagerIndexRetDaily().get().copy()
        mng_index_ret[mng_index_ret > 0] = 0
        self._factor = mng_index_ret.rolling(window=mng_index_ret.shape[0],min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngDownsideStdMonthlyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngDownsideStdMonthlyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexRetMonthly())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index_ret = ManagerIndexRetMonthly().get().copy()
        mng_index_ret[mng_index_ret > 0] = 0
        self._factor = mng_index_ret.rolling(window=mng_index_ret.shape[0],min_periods=self.MIN_TIME_SPAN).std(ddof=1) * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngFundTypeTradingDays(Factor):

    def __init__(self):
        super().__init__(f_name='MngFundTypeTradingDays', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndex())
        self._deps.add(TradingDay())

    def calc(self):
        mng_index = ManagerIndex().get()
        self._factor = mng_index.rolling(window=mng_index.shape[0],min_periods=1).apply(self.rolling_trade_year, raw=True)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClAlphaBetaWeekly1Y(Factor):

    def __init__(self):
        super().__init__(f_name='MngClAlphaBetaWeekly1Y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexWeekly())
        self._deps.add(TradingDay())
        self._deps.add(IndexRetWeekly())

    def loop_item(self, mng_id):
        index_id = mng_id.split('_')[0]
        df = self.mng_weekly_ret[[mng_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={mng_id:'fund',index_id:'benchmark'}).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        pd.Series(df.index).rolling(
            window=52, min_periods=24).apply(
            partial(self.rolling_cl_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{mng_id}', 'beta':f'beta_{mng_id}'})
        return df

    def loop_item_update(self, mng_id):
        index_id = mng_id.split('_')[0]
        df = self.mng_weekly_ret[[mng_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={mng_id:'fund',index_id:'benchmark'}).loc[:self.update_dt].tail(52).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        self._rolling_cl_alpha_beta(res, df[['fund','benchmark']].to_numpy())
        fund_res = {f'alpha_{mng_id}':res[0]['alpha'],
                    f'beta_{mng_id}':res[0]['beta']}   
        return fund_res
    
    def update_one_day(self, dt):
        self.update_dt = dt
        mng_list = self.mng_weekly_ret.columns.tolist()
        res = [self.loop_item_update(i) for i in mng_list]
        dic = {}
        for _i in res:
            if _i is not None:
                dic.update(_i)
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self.mng_weekly_ret = ManagerIndexWeekly().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        last_date = self._exsited_factor.index[-1]
        td = self.index_weekly_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()

    def calc(self, is_multi_cpu=False):
        self.mng_weekly_ret = ManagerIndexWeekly().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        mng_list = self.mng_weekly_ret.columns.tolist()
        # calculate
        result = []
        if is_multi_cpu:
            p = Pool()
            res = [i for i in p.imap_unordered(self.loop_item, mng_list, 64) if i is not None]
            p.close()
            p.join()
            result.extend(res)
        else:
            for mng_id in mng_list:
                res_i = self.loop_item(mng_id)
                if res_i is not None:
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor.index.name = 'datetime'
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClAlphaWeekly1Y(Factor):

    def __init__(self):
        super().__init__(f_name='MngClAlphaWeekly1Y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(MngClAlphaBetaWeekly1Y())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = MngClAlphaBetaWeekly1Y().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.replace('alpha_','') for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClBetaWeekly1Y(Factor):

    def __init__(self):
        super().__init__(f_name='MngClBetaWeekly1Y', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(MngClAlphaBetaWeekly1Y())
        self._deps.add(TradingDay())

    def calc(self):
        self._factor = MngClAlphaBetaWeekly1Y().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.replace('beta_','') for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClAlphaBetaWeeklyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngClAlphaBetaWeeklyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(ManagerIndexWeekly())
        self._deps.add(TradingDay())
        self._deps.add(IndexRetWeekly())

    def loop_item(self, mng_id):
        index_id = mng_id.split('_')[0]
        df = self.mng_weekly_ret[[mng_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={mng_id:'fund',index_id:'benchmark'}).reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        pd.Series(df.index).rolling(
            window=df.shape[0], min_periods=24).apply(
            partial(self.rolling_cl_alpha_beta, res=res, df=df), raw=True)
        df = pd.DataFrame(res,index=df.datetime[-len(res):])
        df = df.rename(columns={'alpha':f'alpha_{mng_id}', 'beta':f'beta_{mng_id}'})
        return df

    def loop_item_update(self, mng_id):
        index_id = mng_id.split('_')[0]
        df = self.mng_weekly_ret[[mng_id]].join(self.index_weekly_ret[[index_id]]).dropna()
        df = df.rename(columns={mng_id:'fund',index_id:'benchmark'}).loc[:self.update_dt].reset_index()
        if df.shape[0] < 24:
            return None
        res = []
        self._rolling_cl_alpha_beta(res, df[['fund','benchmark']].to_numpy())
        fund_res = {f'alpha_{mng_id}':res[0]['alpha'],
                    f'beta_{mng_id}':res[0]['beta']}   
        return fund_res
    
    def update_one_day(self, dt):
        self.update_dt = dt
        mng_list = self.mng_weekly_ret.columns.tolist()
        res = [self.loop_item_update(i) for i in mng_list]
        dic = {}
        for _i in res:
            if _i is not None:
                dic.update(_i)
        return pd.DataFrame([dic], index=[self.update_dt])

    def append_update(self):
        self._exsited_factor = self.get()
        self.mng_weekly_ret = ManagerIndexWeekly().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        last_date = self._exsited_factor.index[-1]
        td = self.index_weekly_ret.index
        update_list = td[td > last_date].tolist()
        _df_list = []
        for dt in update_list:
            res = self.update_one_day(dt)
            _df_list.append(res)
        if _df_list == []:
            return True
        df_update = pd.concat(_df_list,axis=0)
        self._exsited_factor = self._exsited_factor.append(df_update)
        self._factor = self._exsited_factor
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())
        return self.save()
        
    def calc(self, is_multi_cpu=False):
        self.mng_weekly_ret = ManagerIndexWeekly().get()
        self.index_weekly_ret = IndexRetWeekly().get().rename(columns=self.INDEX_DICT)[list(self.INDEX_DICT.values())]
        mng_list = self.mng_weekly_ret.columns.tolist()
        # calculate
        result = []
        if is_multi_cpu:
            p = Pool()
            res = [i for i in p.imap_unordered(self.loop_item, mng_list, 64) if i is not None]
            p.close()
            p.join()
            result.extend(res)
        else:
            for mng_id in mng_list:
                res_i = self.loop_item(mng_id)
                if res_i is not None:
                    result.append(res_i)
        self._factor = pd.concat(result, axis=1)
        self._factor = self._factor.sort_index()
        self._factor.index.name = 'datetime'
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClAlphaWeeklyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngClAlphaWeeklyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(MngClAlphaBetaWeeklyHistory())

    def calc(self):
        self._factor = MngClAlphaBetaWeeklyHistory().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'alpha']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.replace('alpha_','') for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngClBetaWeeklyHistory(Factor):

    def __init__(self):
        super().__init__(f_name='MngClBetaWeeklyHistory', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(MngClAlphaBetaWeeklyHistory())

    def calc(self):
        self._factor = MngClAlphaBetaWeeklyHistory().get()
        col_name = self._factor.columns.tolist()
        factor_list = [i for i in col_name if i.split('_')[0] == 'beta']
        self._factor = self._factor[factor_list]
        name_dic = { i : i.replace('beta_','') for i in factor_list}
        self._factor = self._factor[factor_list].rename(columns=name_dic)
        self._factor = self.data_reindex_daily_trading_day(self._factor, TradingDay().get())

class MngFundSize(Factor):

    def __init__(self):
        super().__init__(f_name='MngFundSize', f_type=FundFactorType.DERIVED, f_level='derived')
        self._deps.add(TradingDay())
        self._deps.add(FundInfo())
        self._deps.add(FundManagerInfo())
        self._deps.add(FundSize())

    def mng_process_fund_ret(self, this_manager_fund_ids, this_manager_info, date_index):
        res = []
        for fund_id in this_manager_fund_ids:
            single_fund_info = this_manager_info.loc[[fund_id]]
            res_i =  self.mng_lambda_filter_date_range(single_fund_info, date_index)
            res_i.name = fund_id
            res.append(res_i)
        return pd.concat(res, axis=1)

    def fund_manager_size_prepare(self):
        self.trading_days_list = TradingDay().get().index
        self.fund_info = FundInfo().get()
        self.fund_manager_info = FundManagerInfo().get()
        self.fund_manager_info = self.fund_manager_info.rename(columns={'mng_id': 'manager_id', 'mng_name': 'name', 'start_date': 'start', 'end_date': 'end'})
        ## 计算基金经理指数时只去掉分级基金子基金， 不能回测交易的基金依然影响基金经理能力
        self.fund_info = self.fund_info[(self.fund_info.structure_type <= 1)
                                        & (~self.fund_info.wind_class_2.isnull())]
        self.fund_size = FundSize().get()
        self.fund_manager_info = self.fund_manager_info.set_index('fund_id')
        self.manager_name_dict = self.fund_manager_info.set_index('manager_id').to_dict()['name'] 

    def calc(self):
        self.fund_manager_size_prepare()
        fund_manager_list = list(self.manager_name_dict.keys())
        t0 = time.time()
        loop_paras = []
        for m_id in fund_manager_list:
            for fund_type in self.FUND_CLASSIFIER:
                loop_paras.append([m_id, fund_type])
        result = []
        for para_i in loop_paras:
            df = self.size_calculation(para_i) 
            result.append(df)
        t1 = time.time()
        print(f'cost time {t1 - t0}')
        self._factor = pd.concat(result,axis=1).dropna(axis=1,how='all')

    def mng_lambda_filter_date_range(self, single_fund_info: pd.DataFrame, date_index: pd.Series) -> pd.Series:
        result: List[pd.Series] = []
        for row in single_fund_info.itertuples(index=False):
            result.append(pd.Series((date_index >= row.start) & (date_index <= row.end), index=date_index))
        return pd.concat(result, axis=1).sum(axis=1)

    def size_calculation(self, para_i):
        m_id = para_i[0]
        fund_type = para_i[1]
        wind_class_2_list = self.FUND_CLASSIFIER[fund_type]
        this_manager_info = self.fund_manager_info[(self.fund_manager_info['wind_class_2'].isin(wind_class_2_list))
                            & (self.fund_manager_info['manager_id'] == m_id)]
        if this_manager_info.shape[0] == 0:
            return None
        index_start_date = this_manager_info.start.min()
        index_end_date = this_manager_info.end.max()
        this_manager_fund_ids = this_manager_info.index.unique().intersection(self.fund_size.columns).tolist()
        if len(this_manager_fund_ids) < 1:
            return None
        fund_size = self.fund_size.loc[index_start_date:index_end_date, this_manager_fund_ids]
        manager_status = self.mng_process_fund_ret(this_manager_fund_ids, this_manager_info, fund_size.index)
        fund_size = fund_size * manager_status
        fund_size = pd.DataFrame(fund_size.sum(axis=1), columns=[f'{fund_type}_{m_id}'])
        return fund_size
