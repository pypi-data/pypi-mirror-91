import datetime
import pandas as pd
import numpy as np
from ...api.raw import RawDataApi
from ..raw.raw_data_helper import RawDataHelper
from ....data.view.raw_models import QSOverseaFundCurMdd, QSOverseaFundMonthlyRet, QSOverseaFundIndicator, QSOverseaFundRadarScore, QSOverseaFundPeriodRet
from ....util.calculator_item import CalculatorBase

class OverseaFundStyleBox:

    def __init__(self, data_helper: RawDataHelper):
        self._data_helper = data_helper
        self._raw_api = RawDataApi()

    def init(self, end_date=str):
        self.fund_info = self._raw_api.get_over_sea_fund_info()
        self.fund_pos = self._raw_api.get_fund_hold_top10_pos()

        self.ch_stock_fin = self._raw_api.get_em_stock_fin_fac(stock_list=[])
        self.hm_stock_fin = self._raw_api.get_os_stock_fin_fac(stock_list=[])

        self.ch_stock_price = self._raw_api.get_em_stock_price(start_date, end_date, columns=['close']).set_index(['stock_id', 'datetime'])
        #self.h_stock_price = self._raw_api.
        #self.m_stock_price = self._raw_api.

    