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

from f4ratk.analyze import Analyzer
from f4ratk.domain import AnalysisConfig
from f4ratk.fama import FamaReader
from f4ratk.shared import Normalizer
from f4ratk.ticker.reader import Stock, read_ticker


def analyze_ticker_symbol(stock: Stock, analysis_config: AnalysisConfig) -> None:
    fama_reader = FamaReader(Normalizer())
    analyzer = Analyzer()

    data = read_ticker(stock=stock, frame=analysis_config.frame)

    analyzer.analyze(
        data,
        fama_reader.fama_data(
            region=analysis_config.region, frequency=analysis_config.frame.frequency
        ),
    )
