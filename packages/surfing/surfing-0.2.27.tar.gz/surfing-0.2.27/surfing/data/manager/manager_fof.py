
from typing import List, Optional, Tuple
import re
import datetime

import numpy as np
import pandas as pd

from ...util.singleton import Singleton
from ...constant import FundStatus, HoldingAssetType
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi
from ..view.basic_models import FOFManually, HedgeFundNAV
from ..view.derived_models import FOFNav
from ..wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector


class FOFDataManager(metaclass=Singleton):

    # 从EXCEL读取数据的路径，一般用不到
    _FILE_PATH = './nav_data/FOF运营计算逻辑.xlsx'

    # TODO: 暂时只支持一个FOF
    _FOF_ID = 'SLW695'

    _FEES_FLAG: List[int] = [1, 1, 1, 1, -1, -1, -1]
    _DAYS_PER_YEAR_FOR_INTEREST = 360

    def __init__(self):
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.float_format', lambda x: '%.4f' % x)
        self._start_date: Optional[str] = None
        self._end_date: Optional[str] = None
        self._date_list: Optional[np.ndarray] = None
        self._fof_scale: Optional[pd.DataFrame] = None
        self._hedge_pos: Optional[pd.DataFrame] = None
        self._hedge_nav: Optional[pd.DataFrame] = None
        self._fund_pos: Optional[pd.DataFrame] = None
        self._manually: Optional[pd.DataFrame] = None
        self._fof_nav: Optional[pd.DataFrame] = None

    def _get_days_this_year_for_fee(self, the_date: datetime.date) -> int:
        '''计算今年一共有多少天'''
        return pd.Timestamp(year=the_date.year, month=12, day=31).dayofyear

    @staticmethod
    def _calc_virtual_net_value():
        '''计算虚拟净值'''
        fund_info = FOFDataManager.get_hedge_fund_info()
        # TODO: 目前只支持高水位法计算
        fund_info = fund_info.loc[fund_info.incentive_fee_mode == '高水位法']
        fund_info = fund_info.set_index('fund_id')

        df = FOFDataManager.get_hedge_fund_nav()
        df = df[df.fund_id.isin(fund_info.index.array)]
        df = df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

        trading_day_list = BasicDataApi().get_trading_day_list(start_date=df.datetime.sort_values().array[0], end_date=datetime.datetime.now().date())
        df = df.pivot(index='datetime', columns='fund_id', values='net_asset_value').reindex(trading_day_list.datetime).ffill()
        # 盈利
        excess_ret = (df - fund_info.water_line)
        # 盈 或 亏
        earn_con = (excess_ret > 0) * 1
        # 费
        pay_mng_fee = excess_ret * earn_con * fund_info.incentive_fee_ratio
        # 净值
        df -= pay_mng_fee
        df = df.round(fund_info.v_nav_decimals)
        return df
        # print(f'do not support the incentive fee mode: {self._INCENTIVE_FEE_MODE}')

    def init(self):
        # 获取fof基本信息
        fof_info: Optional[pd.DataFrame] = FOFDataManager.get_fof_info([FOFDataManager._FOF_ID])
        assert fof_info is not None, f'get fof info for {FOFDataManager._FOF_ID} failed'

        fof_info = fof_info.sort_values(by=['fof_id', 'datetime']).iloc[-1]
        self._MANAGEMENT_FEE_PER_YEAR = fof_info.management_fee
        self._CUSTODIAN_FEE_PER_YEAR = fof_info.custodian_fee
        self._ADMIN_SERVICE_FEE_PER_YEAR = fof_info.administrative_fee
        self._DEPOSIT_INTEREST_PER_YEAR = fof_info.current_depoist_rate
        self._SUBSCRIPTION_FEE = fof_info.subscription_fee
        self._ESTABLISHED_DATE = fof_info.established_date
        self._INCENTIVE_FEE_MODE = fof_info.incentive_fee_mode
        # FIXME 先hard code
        self._LAST_RAISING_PERIOD_INTEREST_DATE = datetime.date(2020, 12, 20)
        print(f'fof info: (id){FOFDataManager._FOF_ID} (management_fee){self._MANAGEMENT_FEE_PER_YEAR} (custodian_fee){self._CUSTODIAN_FEE_PER_YEAR} '
              f'(admin_service_fee){self._ADMIN_SERVICE_FEE_PER_YEAR} (current_deposit_rate){self._DEPOSIT_INTEREST_PER_YEAR} (subscription_fee){self._SUBSCRIPTION_FEE} '
              f'(incentive fee mode){self._INCENTIVE_FEE_MODE}')

        # 获取FOF份额变化信息
        fof_scale = FOFDataManager.get_fof_scale_alteration([FOFDataManager._FOF_ID])
        self._fof_scale = fof_scale.set_index('datetime')
        self._start_date = self._fof_scale.index.min()

        # trading_day_list = BasicDataApi().get_trading_day_list(start_date=self._start_date, end_date=datetime.datetime.now().date())
        # 将昨天作为end_date
        self._end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        print(f'(start_date){self._start_date} (end_date){self._end_date}')
        self._date_list: np.ndarray = pd.date_range(self._start_date, self._end_date).date

        # 获取fof持仓
        positions: Optional[pd.DataFrame] = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
        assert positions is not None, f'get fof pos for {FOFDataManager._FOF_ID} failed'

        # 这里不需要在途的持仓
        positions = positions[positions.status == FundStatus.DONE]

        positions = positions.pivot(index='confirmed_date', columns=['asset_type', 'fund_id'], values='unit_total')
        positions = positions.reindex(index=self._date_list).ffill()
        # 持仓中的公募基金
        try:
            self._fund_pos = positions[HoldingAssetType.MUTUAL]
        except KeyError:
            print('no fund pos found')

        # 持仓中的私募基金
        try:
            self._hedge_pos = positions[HoldingAssetType.HEDGE]
        except KeyError:
            print('no hedge pos found')

        # 获取私募基金净值数据
        hedge_fund_nav = FOFDataManager.get_hedge_fund_nav()
        hedge_fund_nav = hedge_fund_nav.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')
        self._hedge_nav = hedge_fund_nav.pivot(index='datetime', columns='fund_id', values='v_net_value').reindex(index=self._date_list).ffill()

        # 获取人工手工校正信息
        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID])
        self._manually = manually.set_index('datetime')

    def _get_hedge_mv(self) -> float:
        return (self._hedge_nav * self._hedge_pos).round(2).sum(axis=1).fillna(0)

    def _insert_errors_to_db_from_file(self, path: str = ''):
        '''将人工手工校正信息写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        errors: pd.DataFrame = pd.read_excel(path, sheet_name='2-1资产估值表（净值发布）', header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        errors = errors.loc[:, ['每日管理费误差', '每日行政服务费误差', '每日托管费误差']]
        errors = errors.droplevel(level=[0, 2], axis=0).droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        errors = errors.rename_axis(index=['datetime']).reset_index()
        errors = errors.rename(columns={'每日管理费误差': 'management_fee_error', '每日行政服务费误差': 'admin_service_fee_error', '每日托管费误差': 'custodian_fee_error'})
        errors = errors[errors.notna().any(axis=1)].set_index('datetime').sort_index()

        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID]).drop(columns='_update_time')
        manually = manually.set_index('datetime')
        manually = manually.combine_first(errors)
        manually['fof_id'] = FOFDataManager._FOF_ID
        manually = manually.reset_index()
        print(manually)
        manually.to_sql(FOFManually.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _insert_nav_info_to_db_from_file(self, path: str = ''):
        '''将私募基金净值数据写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        nav: pd.DataFrame = pd.read_excel(path, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav.droplevel(level=0)
        nav = nav['私募标的净值']
        nav = nav.loc[(slice(None), 1), :]
        nav = nav.droplevel(level=1)
        nav = nav.stack(0).rename_axis(index=['datetime', 'fund_id'])
        nav = nav.rename(columns={'单位净值': 'net_asset_value', '累计净值': 'acc_unit_value', '虚拟净值': 'v_net_value'})
        nav = nav[nav.notna().any(axis=1)].sort_index(axis=0, level=0).reset_index()
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(one) for one in nav.fund_id]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav['fund_id'] = fund_id_list
        print(nav)
        nav.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _read_data_from_file(self):
        # 解析私募基金净值数据
        nav: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav['私募标的净值']
        nav = nav.swaplevel(axis=1)
        nav = nav['虚拟净值']
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in nav.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav = nav.set_axis(labels=fund_id_list, axis=1)
        nav = nav.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        nav = nav[nav.trading_flag == 1]
        nav = nav.drop(columns=['id', 'trading_flag']).set_index('datetime')
        nav = nav.set_axis(pd.to_datetime(nav.index, infer_datetime_format=True).date, axis=0)
        nav = nav[nav.notna().any(axis=1)].sort_index()

        # 解析持仓公募基金数据
        whole_pos: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        mutual_fund_pos = whole_pos.loc[:, ('公募标的（份额）', slice(None), '份额')]
        mutual_fund_pos = mutual_fund_pos.droplevel(level=[0, 2], axis=1)
        mutual_fund_pos = mutual_fund_pos.loc[:, mutual_fund_pos.notna().any(axis=0)]
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in mutual_fund_pos.columns]
        assert None not in fund_id_list, 'parse mutual fund id failed!!'
        fund_id_list = [one.group(1) + '!0' for one in fund_id_list]
        mutual_fund_pos = mutual_fund_pos.set_axis(labels=fund_id_list, axis=1)
        mutual_fund_pos = mutual_fund_pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        mutual_fund_pos = mutual_fund_pos[mutual_fund_pos.trading_flag == 1]
        mutual_fund_pos = mutual_fund_pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        mutual_fund_pos = mutual_fund_pos.set_axis(pd.to_datetime(mutual_fund_pos.index, infer_datetime_format=True).date, axis=0)
        self._fund_pos = mutual_fund_pos[mutual_fund_pos.notna().any(axis=1)].sort_index()
        self._start_date = self._fund_pos.index.min()
        self._end_date = self._fund_pos.index.max()
        print(f'start date: {self._start_date}')
        print(f'end date: {self._end_date}')

        # 解析持仓私募基金数据
        pos: pd.DataFrame = whole_pos.loc[:, '私募标的']
        pos = pos.swaplevel(axis=1)
        pos = pos['份额']
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in pos.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        pos = pos.set_axis(labels=fund_id_list, axis=1)
        pos = pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        pos = pos[pos.trading_flag == 1]
        pos = pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        pos = pos.set_axis(pd.to_datetime(pos.index, infer_datetime_format=True).date, axis=0)
        pos = pos[pos.notna().any(axis=1)].sort_index()
        self._hedge_nav = nav
        self._hedge_pos = pos

        # 解析杂项费用、收入数据
        misc_fees: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        misc_fees = misc_fees.loc[:, ['银行活期', '在途资金', '累计应收银行\n存款利息', '应收募集期\n利息', '累计计提\n管理费\n（修正）', '累计计提行政\n服务费\n（修正）', '累计计提\n托管费\n（修正）']]
        misc_fees = misc_fees.droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        misc_fees = misc_fees.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        misc_fees = misc_fees[misc_fees.trading_flag == 1]
        misc_fees = misc_fees.drop(columns=['id', 'trading_flag']).set_index('datetime')
        misc_fees = misc_fees.set_axis(pd.to_datetime(misc_fees.index, infer_datetime_format=True).date, axis=0)
        misc_fees = misc_fees[misc_fees.notna().any(axis=1)].sort_index()
        self._misc_fees = (misc_fees * FOFDataManager._FEES_FLAG).fillna(0).sum(axis=1)

        # 解析投资人持仓数据
        investor_share: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name='4-2投资人份额变更表', header=0, index_col='到账日期', parse_dates=True)
        investor_share = investor_share.rename_axis(index='datetime')
        self._investor_share = investor_share['确认份额'].groupby(level=0).sum().cumsum()

    def calc_nav(self, is_from_excel=False):
        if is_from_excel:
            self._read_data_from_file()
        else:
            self.init()

        # 根据公募基金持仓获取相应基金的净值
        fund_nav: Optional[pd.DataFrame] = BasicDataApi().get_fund_nav_with_date_range(start_date=self._start_date, end_date=self._end_date, fund_list=self._fund_pos.columns.to_list())
        assert fund_nav is not None, f'get fund nav of {self._fund_pos.columns.to_list()} failed'
        fund_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='unit_net_value')
        fund_nav = fund_nav.reindex(index=self._date_list).ffill()
        # 公募基金总市值
        fund_mv: pd.DataFrame = (self._fund_pos * fund_nav).round(2).sum(axis=1).fillna(0)

        if is_from_excel:
            # 净资产 = 公募基金总市值 + 私募基金总市值 + 其他各项收入、费用的净值
            net_assets = fund_mv.add(self._get_hedge_mv(), fill_value=0).add(self._misc_fees, fill_value=0)
            print(net_assets)

            # NAV = 净资产 / 总份额
            investor_share = self._investor_share.reindex(index=net_assets.index).ffill()
            self._fof_nav = net_assets / investor_share
            print(self._fof_nav.round(4))
        else:
            # 获取FOF资产配置信息
            asset_alloc = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
            asset_alloc = asset_alloc.set_index('datetime')

            hedge_fund_mv = self._get_hedge_mv()

            # 循环遍历每一天来计算
            shares_list = pd.Series(dtype='float64', name='share')
            cash_list = pd.Series(dtype='float64', name='cash')
            fof_nav_list = pd.Series(dtype='float64', name='nav')
            today_fund_mv_list = pd.Series(dtype='float64', name='total_fund_mv')
            today_hedge_mv_list = pd.Series(dtype='float64', name='total_hedge_mv')
            net_assets_list = pd.Series(dtype='float64', name='net_asset')
            net_assets_fixed_list = pd.Series(dtype='float64', name='net_asset_fixed')
            misc_fees_list = pd.Series(dtype='float64', name='misc_fees')
            misc_amount_list = pd.Series(dtype='float64', name='misc_amount')
            deposit_interest_list = pd.Series(dtype='float64', name='deposit_interest')
            trades_in_transit = []
            deposit_in_transit = []
            total_cash = 0
            for date in self._date_list:
                try:
                    # 看看当天有没有买入FOF
                    # TODO: 暂不支持处理赎回
                    scale_data = self._fof_scale.loc[[date], :]
                except KeyError:
                    # 处理没有买入的情况
                    # 申购金额为0
                    total_amount = 0
                    # 份额增加为0
                    share_increased = 0
                    if not cash_list.empty:
                        # 如果不是计算的第一天，则total_cash到这里仍与头一天相同
                        total_cash = cash_list.iat[-1]
                else:
                    # 汇总今天所有的申购资金
                    total_amount = scale_data.amount.sum()
                    try:
                        # 用申购金额除以确认日的净值以得到份额
                        share_increased = total_amount / (1 + self._SUBSCRIPTION_FEE) / fof_nav_list.at[scale_data.iloc[0, :].confirmed_date]
                    except KeyError:
                        # 没有fof的净值数据，以1作为净值
                        share_increased = total_amount / (1 + self._SUBSCRIPTION_FEE)

                    # 获得银行活期存款
                    if cash_list.empty:
                        # 如果是计算的第一天，认购金额即为银行活期存款
                        total_cash = total_amount
                    else:
                        deposited_date = scale_data.iloc[0, :].deposited_date
                        if date == deposited_date:
                            # 如果和deposited date是同一天，直接将total_amount加到银行活期存款中
                            total_cash = cash_list.iat[-1] + total_amount
                        else:
                            # 如果不是，需要稍后再计算，同时银行活期存款与头一天相同
                            total_cash = cash_list.iat[-1]
                            deposit_in_transit.append((deposited_date, total_amount))
                finally:
                    total_cash = round(total_cash, 2)
                    share_increased = round(share_increased, 2)

                # 这个日期之后才正式成立，所以在此之前都不需要处理后续步骤
                if date < self._ESTABLISHED_DATE:
                    cash_list.loc[date] = total_cash
                    if share_increased > 0:
                        shares_list.loc[date] = share_increased
                    continue

                # 计算那些仍然在途的入金
                deposit_done = []
                deposit_amount_in_transit = 0
                for one in deposit_in_transit:
                    if one[0] == date:
                        # 到了deposited_date，计入银行活期存款然后后续删除该记录
                        deposit_done.append(deposit_in_transit.index(one))
                        total_cash += one[1]
                    else:
                        # 如果没到，也要把他们统计进来，不计算利息，但应该计入净资产中
                        deposit_amount_in_transit += one[1]
                for one in deposit_done:
                    del deposit_in_transit[one]

                try:
                    # 看看当天有没有投出去，继而产生在途资金
                    # TODO: 暂不支持赎回
                    cash_in_transit = 0
                    today_asset_alloc = asset_alloc.loc[[date], :]
                    for row in today_asset_alloc.itertuples():
                        if not pd.isnull(row.amount):
                            cash_in_transit += row.amount
                            if row.confirmed_date != row.Index or row.status == FundStatus.IN_TRANSIT:
                                # 如果没有到confirmed_date或状态是仍然在途，需要把它们记下来
                                trades_in_transit.append((row.Index, row.confirmed_date, row.amount))
                        if not pd.isnull(row.share):
                            # 业绩报酬计提扣除份额完成
                            if row.status == FundStatus.INSENTIVE_DONE:
                                self._hedge_pos.loc[self._hedge_pos.index>=date, row.fund_id] -= row.share
                                # 重刷hedge_fund_mv
                                hedge_fund_mv = self._get_hedge_mv()
                    assert total_cash >= cash_in_transit, f'no enough cash to buy asset!! (date){date} (total cash){total_cash} (cash in transit){cash_in_transit}'
                    total_cash -= cash_in_transit
                except KeyError:
                    cash_in_transit = 0

                # 计算那些仍然在途的资金
                trades_done = []
                for one in trades_in_transit:
                    # 当天就不处理了(在上边处理过了)
                    if one[0] == date:
                        continue
                    if one[1] is not None:
                        if date >= one[1]:
                            # 到confirmed_date了，把这些记录记下来，后续可以删除
                            trades_done.append(trades_in_transit.index(one))
                            # confirmed当天就不把amount计进来了
                            if date == one[1]:
                                continue
                    cash_in_transit += one[2]
                for one in trades_done:
                    del trades_in_transit[one]
                cash_in_transit = round(cash_in_transit, 2)

                # 应收募集期利息 TODO 暂时先hard code了
                if date <= self._LAST_RAISING_PERIOD_INTEREST_DATE:
                    raising_period_interest = 77.78
                else:
                    raising_period_interest = 0
                # 计提管理费, 计提行政服务费, 计提托管费
                if not net_assets_list.empty:
                    misc_fees = (net_assets_list.iat[-1] * pd.Series([self._MANAGEMENT_FEE_PER_YEAR, self._CUSTODIAN_FEE_PER_YEAR, self._ADMIN_SERVICE_FEE_PER_YEAR]) / self._get_days_this_year_for_fee(date)).round(2).sum()
                else:
                    misc_fees = 0

                # 处理人工手工校正的一些数据
                try:
                    fee_transfer = self._manually.at[date, 'fee_transfer']
                    if not pd.isnull(fee_transfer):
                        fee_transfer = round(fee_transfer, 2)
                        # 现金里扣掉的同时 累计计提费用也相应扣掉
                        total_cash += fee_transfer
                        misc_fees += fee_transfer
                except KeyError:
                    pass

                try:
                    cd_interest_transfer = self._manually.at[date, 'cd_interest_transfer']
                    if not pd.isnull(cd_interest_transfer):
                        cd_interest_transfer = round(cd_interest_transfer, 2)
                        # 扣掉累计应收银行存款利息
                        total_cash += cd_interest_transfer
                except KeyError:
                    pass

                try:
                    other_fees = self._manually.at[date, 'other_fees']
                    if not pd.isnull(other_fees):
                        other_fees = round(other_fees, 2)
                        # 只在现金里扣掉
                        total_cash += other_fees
                except KeyError:
                    pass
                cash_list.loc[date] = total_cash

                # 应收银行存款利息
                deposit_interest = round(cash_list.iat[-1] * self._DEPOSIT_INTEREST_PER_YEAR / self._DAYS_PER_YEAR_FOR_INTEREST, 2)

                # 记录一些信息
                # TODO: 这里也需要在费用划拨时进行相应的扣除
                if deposit_interest_list.empty:
                    deposit_interest_list.loc[date] = deposit_interest
                else:
                    deposit_interest_list.loc[date] = deposit_interest_list.iat[-1] + deposit_interest

                if misc_fees_list.empty:
                    misc_fees_list.loc[date] = misc_fees
                else:
                    misc_fees_list.loc[date] = misc_fees_list.iat[-1] + misc_fees
                misc_amount = total_cash + cash_in_transit + deposit_amount_in_transit + deposit_interest_list.iat[-1] + raising_period_interest - misc_fees_list.iat[-1]
                misc_amount_list.loc[date] = misc_amount

                # 获取持仓中当日公募、私募基金的MV
                try:
                    today_fund_mv = fund_mv.loc[date]
                except KeyError:
                    today_fund_mv = 0
                today_fund_mv_list.loc[date] = today_fund_mv
                try:
                    today_hedge_mv = hedge_fund_mv.loc[date]
                except KeyError:
                    today_hedge_mv = 0
                today_hedge_mv_list.loc[date] = today_hedge_mv
                # 计算净资产
                today_net_assets = today_fund_mv + today_hedge_mv + misc_amount
                net_assets_list.loc[date] = today_net_assets

                # 计算修正净资产
                try:
                    errors_to_be_fixed = self._manually.loc[self._manually.index <= date, ['admin_service_fee_error', 'custodian_fee_error', 'management_fee_error']].round(2).sum(axis=1).sum()
                except KeyError:
                    errors_to_be_fixed = 0
                today_net_assets_fixed = today_net_assets + errors_to_be_fixed
                net_assets_fixed_list.loc[date] = today_net_assets_fixed

                # 如果今日有投资人申购fof 记录下来
                if share_increased > 0:
                    shares_list.loc[date] = share_increased
                # 计算fof的nav
                if shares_list.sum() != 0:
                    fof_nav = today_net_assets_fixed / shares_list.sum()
                else:
                    fof_nav = 1
                fof_nav_list.loc[date] = round(fof_nav, 4)
            # 汇总所有信息
            total_info = pd.concat([shares_list, cash_list, fof_nav_list, today_fund_mv_list, today_hedge_mv_list, net_assets_list, net_assets_fixed_list, misc_amount_list, misc_fees_list, deposit_interest_list], axis=1).sort_index()
            print(total_info)
            self._fof_nav = fof_nav_list.rename_axis('datetime').to_frame(name='nav').reset_index()
            self._fof_nav['fof_id'] = FOFDataManager._FOF_ID

    def dump_fof_nav_to_db(self):
        if self._fof_nav is not None:
            now_df = DerivedDataApi().get_fof_nav([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['_update_time'])
                # merge on all columns
                df = self._fof_nav.merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_nav
            for date in df.datetime.unique():
                DerivedDataApi().delete_fof_nav(date_to_delete=date, fund_list=df[df.datetime == date].fof_id.to_list())
            df.to_sql(FOFNav.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_to_db] done')
        else:
            print('[dump_fof_nav_to_db] no nav, should calc it first')

    def service_start(self):
        import os
        from ...util.mail_retriever import MailAttachmentRetriever, IMAP_SPType
        from ..nav_reader.hedge_fund_nav_reader import HedgeFundNAVReader

        try:
            email_data_dir = os.environ['EMAIL_DATA_DIR']
            user_name = os.environ['EMAIL_USER_NAME']
            password = os.environ['EMAIL_PASSWORD']
        except KeyError as e:
            import sys
            sys.exit(f'can not found enough params in env (e){e}')

        mar = MailAttachmentRetriever(email_data_dir)
        new_nav = mar.get_excels(IMAP_SPType.IMAP_QQ, user_name, password)
        if new_nav is not None and new_nav:
            print(new_nav)
            hf_nav_r = HedgeFundNAVReader(email_data_dir, user_name, password)
            hf_nav_r.read_navs_and_dump_to_db()

        self.calc_nav()
        # self.dump_fof_nav_to_db()

    @staticmethod
    def _concat_assets_price(main_asset: pd.DataFrame, secondary_asset: pd.Series) -> pd.DataFrame:
        # FIXME 理论上任意资产在任意交易日应该都是有price的 所以这里的判断应该是可以确保之后可以将N种资产的price接起来
        secondary_asset = secondary_asset[secondary_asset.index <= main_asset.datetime.array[0]]
        # 将price对齐
        secondary_asset /= (secondary_asset.array[-1] / main_asset.nav.array[0])
        # 最后一个数据是对齐用的 这里就不需要了
        return pd.concat([main_asset.set_index('datetime'), secondary_asset.iloc[:-1].to_frame('nav')], verify_integrity=True).sort_index().reset_index()

    # 以下是一些获取数据的接口
    @staticmethod
    def get_fof_info(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_info(fof_id)

    @staticmethod
    def get_fof_asset_allocation(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_asset_allocation(fof_id)

    @staticmethod
    def get_fof_scale_alteration(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_scale_alteration(fof_id)

    @staticmethod
    def get_fof_nav(fof_id: str, *, ref_index_id: str = '', ref_fund_id: str = '') -> Optional[pd.DataFrame]:
        fof_nav = DerivedDataApi().get_fof_nav([fof_id])
        if fof_nav is None or fof_nav.empty:
            return
        fof_nav = fof_nav.drop(columns=['_update_time', 'fof_id'])
        if ref_index_id:
            index_price = BasicDataApi().get_index_price(index_list=[ref_index_id])
            if index_price is None or index_price.empty:
                print(f'[get_fof_nav] get price of index {ref_index_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, index_price.drop(columns=['_update_time', 'index_id']).set_index('datetime')['close'])
        elif ref_fund_id:
            fund_nav = BasicDataApi().get_fund_nav_with_date(fund_list=[ref_fund_id])
            if fund_nav is None or fund_nav.empty:
                print(f'[get_fof_nav] get nav of fund {ref_fund_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, fund_nav.drop(columns='fund_id').set_index('datetime')['adjusted_net_value'])
        else:
            return fof_nav

    @staticmethod
    def get_hedge_fund_info(fund_id: Tuple[str] = ()):
        return BasicDataApi().get_hedge_fund_info(fund_id)

    @staticmethod
    def get_hedge_fund_nav(fund_id: Tuple[str] = ()):
        df = BasicDataApi().get_hedge_fund_nav(fund_id)
        return df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

    # TODO: 提供接口支持对数据的修改


if __name__ == "__main__":
    fof_dm = FOFDataManager()
    fof_dm.service_start()
