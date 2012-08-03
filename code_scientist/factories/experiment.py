#    Copyright (C) 2012 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml

from code_scientist import experiment

import analyzer
import instrument
import report
import target

def create_experiment(definition):
    tgt = target.create_target(definition.get('target_spec'))
    instruments = instrument.create_instruments(
            definition.get('measurement_spec', tgt))
    analyzers = analyzer.create_analyzers(
            definition.get('analysis_spec', tgt, instruments))
    report_generators = report_generator.create_report_generators(
            definition.get('report_spec', tgt, instruments, analyzers))

    return experiment.Experiment(target=tgt, instruments=instruments,
            analyzers=analyzers, report_generators=report_generators)

def create_experiment_from_yaml_filename(filename):
    return create_experiment(yaml.load(open(filename)))
