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

import logging
import yaml

import code
import instrument
import report

from code_scientist import strategy

def parse_input(filename):
    with open(filename) as f:
        logging.debug('Parsing input file.')
        definitions = yaml.load(f.read())
        logging.debug('Input file successfully parsed.')
    return build_strategy(definitions)

def build_strategy(definitions):
    logging.debug('Building graph from definitions.')
    target = code.create_code(definitions.get('code'))
    metrics = instrument.create_instruments(definitions.get('metrics'))
    reporters = report.create_reporters(definitions.get('reports'))

    return strategy.Strategy(target, metrics, reporters)
