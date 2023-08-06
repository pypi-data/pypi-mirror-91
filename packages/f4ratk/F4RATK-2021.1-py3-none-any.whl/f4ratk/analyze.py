##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from logging import getLogger

import pandas
from pandas import DataFrame
from statsmodels.formula import api as sm
from statsmodels.iolib.summary2 import summary_col
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.shared import first_period, last_period

log = getLogger(__name__)


class Analyzer:
    def analyze(self, stock_data: DataFrame, fama_data: DataFrame):
        log.info(
            f"Stock data range: {first_period(stock_data)} - {last_period(stock_data)}"
        )
        log.info(
            f"Fama data range : {first_period(fama_data)} - {last_period(fama_data)}"
        )

        combined: DataFrame = pandas.merge(
            stock_data, fama_data, left_index=True, right_index=True
        )

        log.info(
            f"Result date range: {first_period(combined)} - {last_period(combined)}"
        )

        combined['XsRet'] = combined['Returns'] - combined['RF']

        capm = self._model(formula='XsRet ~ MKT', data=combined)
        ff3 = self._model(formula='XsRet ~ MKT + SMB + HML', data=combined)
        ff5 = self._model(formula='XsRet ~ MKT + SMB + HML + RMW + CMA', data=combined)
        ff6 = self._model(
            formula='XsRet ~ MKT + SMB + HML + RMW + CMA + WML', data=combined
        )

        summary = summary_col(
            [capm, ff3, ff5, ff6],
            stars=True,
            model_names=['CAPM', 'FF3', 'FF5', 'FF6'],
            info_dict={
                'N': lambda x: "{0:d}".format(int(x.nobs)),
            },
            regressor_order=['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML'],
        )

        print(summary)
        print(ff6.summary())

    def _model(self, formula: str, data: DataFrame) -> RegressionResultsWrapper:
        return sm.ols(formula=formula, data=data).fit()
