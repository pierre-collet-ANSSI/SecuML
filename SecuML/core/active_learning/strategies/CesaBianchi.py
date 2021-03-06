# SecuML
# Copyright (C) 2016-2018  ANSSI
#
# SecuML is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SecuML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with SecuML. If not, see <http://www.gnu.org/licenses/>.

from SecuML.core.tools.plots.PlotDataset import PlotDataset

from .queries.CesaBianchiQueries import CesaBianchiQueries
from .Strategy import Strategy


class CesaBianchi(Strategy):

    def __init__(self, iteration):
        Strategy.__init__(self, iteration)
        self.setQueries()

    def setQueries(self):
        b = self.iteration.conf.b
        num_annotations = self.iteration.conf.batch
        self.annotations = CesaBianchiQueries(self.iteration, b,
                                              num_annotations)

    def generateQueries(self):
        self.annotations.run()
        self.generate_queries_time = self.annotations.generate_queries_time

    def annotateAuto(self):
        self.annotations.annotateAuto()

    def getManualAnnotations(self):
        self.annotations.getManualAnnotations()

    #############################
    # Execution time monitoring #
    #############################

    def executionTimeHeader(self):
        header = ['binary_model']
        header.extend(Strategy.executionTimeHeader(self))
        return header

    def executionTimeMonitoring(self):
        line = [self.iteration.update_model.times['binary']]
        line.extend(Strategy.executionTimeMonitoring(self))
        return line

    def executionTimeDisplay(self):
        binary_model = PlotDataset(None, 'Binary model')
        v = [binary_model]
        v.extend(Strategy.executionTimeDisplay(self))
        return v
