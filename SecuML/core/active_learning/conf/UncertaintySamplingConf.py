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

from . import ActiveLearningConfFactory
from .ActiveLearningConf import ActiveLearningConf

from SecuML.core.active_learning.strategies.UncertaintySampling \
        import UncertaintySampling
from SecuML.core.classification.conf.ClassificationConf \
        import ClassificationConf
from SecuML.core.Conf import exportFieldMethod


class UncertaintySamplingConf(ActiveLearningConf):

    def __init__(self, auto, budget, batch, binary_model_conf, validation_conf,
                 logger):
        ActiveLearningConf.__init__(self, auto, budget, validation_conf,
                                    {'binary': binary_model_conf},
                                    logger)
        self.query_strategy = 'UncertaintySampling'
        self.batch = batch

    def getStrategy(self, iteration):
        return UncertaintySampling(iteration)

    def get_exp_name(self):
        name = ActiveLearningConf.get_exp_name(self)
        name += '__batch_%d' % self.batch
        return name

    @staticmethod
    def from_json(obj, logger):
        validation_conf = ActiveLearningConf.validation_conf_from_json(obj,
                                                                       logger)
        binary_model_conf = ClassificationConf.from_json(
                                                obj['models_conf']['binary'],
                                                logger)
        return UncertaintySamplingConf(obj['auto'], obj['budget'],
                                       obj['batch'], binary_model_conf,
                                       validation_conf, logger)

    def fieldsToExport(self):
        fields = ActiveLearningConf.fieldsToExport(self)
        fields.extend([('batch', exportFieldMethod.primitive)])
        return fields

    @staticmethod
    def generateParser(parser):
        al_group = ActiveLearningConf.generateParser(parser,
                                                     classifier_conf=True)
        al_group.add_argument('--batch',
                              type=int,
                              default=100,
                              help='Number of annotations asked from the user '
                                   'at each iteration.')


    @staticmethod
    def fromArgs(args, logger):
        binary_model_conf = ActiveLearningConf.binaryModelConfFromArgs(args,
                                                                       logger)
        validation_conf = ActiveLearningConf.validation_conf_from_args(args,
                                                                       logger)
        return UncertaintySamplingConf(args.auto, args.budget, args.batch,
                                       binary_model_conf, validation_conf,
                                       logger)


ActiveLearningConfFactory.getFactory().registerClass('UncertaintySamplingConf',
                                                     UncertaintySamplingConf)
