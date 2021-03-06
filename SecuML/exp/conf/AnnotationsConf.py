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

from enum import Enum

from SecuML.core.Conf import Conf
from SecuML.core.Conf import exportFieldMethod


class AnnotationsTypes(Enum):
    none = 0
    ground_truth = 1
    partial = 2


class AnnotationsConf(Conf):

    def __init__(self, annotations_filename, annotations_id, logger):
        Conf.__init__(self, logger)
        self.annotations_filename = annotations_filename
        self.annotations_id       = None
        self.annotations_type     = None
        if annotations_id is not None:
            self.set_annotations_id(annotations_id)
        else:
            self.set_annotations_filename(annotations_filename)

    def fieldsToExport(self):
        return [('annotations_id', exportFieldMethod.primitive),
                ('annotations_type', exportFieldMethod.enum_value),
                ('annotations_filename', exportFieldMethod.primitive)]

    def set_annotations_id(self, annotations_id):
        self.annotations_id = annotations_id

    def set_exp_annotations(self, annotations_id, annotations_type):
        self.annotations_id = annotations_id
        self.annotations_type = annotations_type

    def set_annotations_filename(self, annotations_filename):
        self.annotations_filename = annotations_filename
        self.set_annotations_type()

    def set_annotations_type(self):
        if self.annotations_filename is None:
            self.annotations_type = AnnotationsTypes.none
        elif self.annotations_filename == 'ground_truth.csv':
            self.annotations_type = AnnotationsTypes.ground_truth
        else:
            self.annotations_type = AnnotationsTypes.partial

    @staticmethod
    def generateParser(parser, default=None, required=False, message=None):
        if message is None:
            message = 'CSV file containing annotations.'
        parser.add_argument('--annotations', '-a',
                            dest='annotations_file',
                            default=default,
                            required=required,
                            help=message)

    @staticmethod
    def from_json(conf_json, logger):
        conf = AnnotationsConf(conf_json['annotations_filename'],
                               conf_json['annotations_id'],
                               logger)
        conf.annotations_type = AnnotationsTypes[conf_json['annotations_type']]
        return conf
