import datetime
import pandas as pd
import numpy as np
from ...api.raw import RawDataApi
from ..raw.raw_data_helper import RawDataHelper
from ....data.view.raw_models import QSOverseaFundCurMdd, QSOverseaFundMonthlyRet, QSOverseaFundIndicator, QSOverseaFundRadarScore, QSOverseaFundPeriodRet
from ....util.calculator_item import CalculatorBase

# TODO 按照一只美股持仓基金和中国股票持仓基金跑流程
TEST_CODE = ['HKAACE01','HKAAVP'] # 净值分析 持仓分析 选用的基金id
TEST_CODE_COMPARE = ['MXAPJ', 'MXWD', 'MXCNANM', 'RIY'] # 因子计算截面对比 选用的指数id


class OverseaFundNavAnalysis:

    def __init__(self, data_helper: RawDataHelper):
        self._data_helper = data_helper
        self._raw_api = RawDataApi()

    def init(self, end_date=str):
        fund_info = self._raw_api.get_over_sea_fund_info()
        fund_benchmark = self._raw_api.get_over_sea_fund_benchmark()
        # TODO 按照 desc_name 合并会出现小于100只基金信息匹配不上， fund_info 需要补isin
        self.fund_info = pd.merge(fund_info, fund_benchmark[['benchmark_1','benchmark_2','isin_code']], on='isin_code').set_index('codes')
        self.fund_list = TEST_CODE
        self.index_list = TEST_CODE_COMPARE
        _fund_whole_list = self.fund_info[(self.fund_info.fund_type == '股票基金') & (self.fund_info.benchmark_1.isin(self.index_list))].index.tolist()
        self.fund_nav = self._raw_api.get_oversea_fund_nav(end_date=end_date, fund_ids=_fund_whole_list)
        self.index_price = self._raw_api.get_oversea_index_price(end_date=end_date, index_id=self.index_list)
        self.fund_nav = self.fund_nav.pivot_table(index='datetime',columns='codes',values='nav').ffill()
        self.index_price = self.index_price.pivot_table(index='datetime',columns='codes',values='close').ffill()

    def rolling_cur_mdd(self, x):
        if pd.isnull(x).all():
            return np.nan
        x_max = np.fmax.accumulate(x, axis=0)
        return -(1 - np.nanmin(x[-1] / x_max))

    def period_ret_calc(self, df, rule='1M'):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'date'
        fund_id = df.columns.tolist()[0]
        df.columns=['ret']
        df = df.pct_change(1).reset_index()
        if rule == '1M':
            df.date = [i.year * 100 + i.month for i in df.date]
        else:
            df.date = [i.year for i in df.date]
        df.loc[:,'codes'] = fund_id
        return df.dropna(axis=0)

    def process_current_mdd(self):
        _df = self.fund_nav.rolling(window=self.fund_nav.shape[0],min_periods=2).apply(self.rolling_cur_mdd, raw=True)
        _df = pd.DataFrame(_df.stack())
        _df.columns=['current_mdd']
        _df = _df.reset_index()
        self._data_helper._upload_raw(_df, QSOverseaFundCurMdd.__table__.name)
        return _df

    def process_monthly_ret(self):
        _df = self.fund_nav.set_axis(pd.to_datetime(self.fund_nav.index), inplace=False).resample('1M').last()
        _df.index = [i.date() for i in _df.index]
        _df.index.name = 'datetime'
        _df = _df.pct_change(1)
        _df = pd.DataFrame(_df.stack())
        _df.columns=['monthly_ret']
        _df = _df.reset_index()
        self._data_helper._upload_raw(_df, QSOverseaFundMonthlyRet.__table__.name)
        return _df

    def process_indicators(self):
        res = []
        monthly_indicator = []
        daily_indicator = ['start_date','end_date','trade_year','last_unit_nav','cumu_ret','annual_ret','annual_vol','sharpe','recent_1w_ret','recent_1m_ret','recent_3m_ret','recent_6m_ret','recent_1y_ret','recent_3y_ret','recent_5y_ret','worst_3m_ret','worst_6m_ret','last_mv_diff','last_increase_rate','recent_drawdown','recent_mdd_date1','recent_mdd_lens','mdd','mdd_date1','mdd_date2','mdd_lens']
        for fund_id in self.fund_nav:
            fund_nav_i = self.fund_nav[[fund_id]]
            benchmark_id = self.fund_info.loc[fund_id].benchmark_1
            fund_nav_i = fund_nav_i.join(self.index_price[benchmark_id]).ffill().dropna()
            fund_nav_i.columns = ['fund','benchmark']
            last_day = fund_nav_i.index.values[-1]
            # 不同年度
            for year in [1,3,5]:
                b_d = last_day - datetime.timedelta(days=365*year)
                _fund_nav_i = fund_nav_i.loc[b_d:]
                res_i_m = CalculatorBase.get_stat_result(
                        dates = _fund_nav_i.index.values,
                        values = _fund_nav_i.fund.values,
                        risk_free_rate=0.015,
                        frequency='1M',
                        ret_method='pct_ret',
                        benchmark_values=_fund_nav_i.benchmark.values,
                    )
                res_i_d = CalculatorBase.get_stat_result(
                                dates = _fund_nav_i.index.values,
                                values = _fund_nav_i.fund.values,
                                risk_free_rate=0.015,
                                frequency='1D',
                                ret_method='pct_ret',
                                benchmark_values=_fund_nav_i.benchmark.values,
                            )
                _df_i_daily = pd.DataFrame([res_i_d])
                _df_i_monthly = pd.DataFrame([res_i_m])
                # 日度和月度结合
                if monthly_indicator == []:
                    monthly_indicator = [i for i in _df_i_daily.columns if i not in daily_indicator]
                _df_i = pd.concat([_df_i_daily[daily_indicator], _df_i_monthly[monthly_indicator]],axis=1)
                _df_i.loc[:,'codes'] = fund_id
                _df_i.loc[:,'data_cycle'] = year
                res.append(_df_i)
        _df = pd.concat(res)
        _df = _df.drop(columns=['start_date']).rename(columns={'end_date':'datetime'})
        self._data_helper._upload_raw(_df, QSOverseaFundIndicator.__table__.name)
        return _df

    def process_radar_score(self):
        _df = self._raw_api.get_qs_fund_indicator()
        _df = _df[_df.data_cycle == 5].drop(columns=['data_cycle']).set_index('codes')
        _dt = _df.datetime.unique().tolist()[0]
        dic = {
                    'annual_ret':'ret_ability',
                    'annual_vol':'risk_ability',
                    'up_capture':'bull_ability',
                    'down_capture':'bear_ability',
                    'alpha':'alpha_ability',
                    'mdd':'drawdown_ability',}
        _df = _df[list(dic.keys())].rename(columns=dic)
        _df['risk_ability'] = - _df['risk_ability']
        _df['bear_ability'] = - _df['bear_ability']
        _df['drawdown_ability'] = - _df['drawdown_ability']
        _df = (_df.rank(pct=True) / 0.2).astype(int)
        _df['total_score'] = _df.mean(axis=1)
        _df = _df.reset_index()
        _df.loc[:,'datetime'] = _dt
        self._data_helper._upload_raw(_df, QSOverseaFundRadarScore.__table__.name)
        return _df
    
    def process_period_ret(self):
        res = []
        for fund_id in self.fund_nav:
            fund_nav_i = self.fund_nav[[fund_id]]
            # monthly
            res_monthly = self.period_ret_calc(fund_nav_i, rule='1M')
            # yearly
            res_yearly = self.period_ret_calc(fund_nav_i, rule='1Y')
            res.append(res_monthly)
            res.append(res_yearly)
        df = pd.concat(res, axis=0)
        self._data_helper._upload_raw(df, QSOverseaFundPeriodRet.__table__.name)
        return df