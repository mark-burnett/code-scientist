#!/usr/bin/env python
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

import argparse
import csv
import logging.config

from code_scientist import database

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('repository_name', type=str,
            help='Name of repository to measure')
    parser.add_argument('--metric_name', type=str,
            default='sloc', help='Metric to report')
    parser.add_argument('--output_filename', type=str,
            default='report.csv', help='Destination csv file')
    parser.add_argument('file_set_names', metavar='file_set_name',
            type=str, nargs="+", help='File set category to report on')

    parser.add_argument('--config', type=str, default='cs.ini',
            help='Logging configuration.')
    parser.add_argument('--database_url', type=str,
            default='sqlite://db.sqlite', help='SQLAlchemy database URL.')

    return parser.parse_args()

def setup_logging(filename):
    logging.config.fileConfig(filename)

def gather_metrics(repository_name, metric_name, file_set_names):
    logging.debug('Gathering metrics.')

    dbs = database.Session()
    repository = dbs.query(database.Repository
            ).filter_by(name=repository_name).one()
    logging.debug('Got repository id = %d', repository.id)
    metric = dbs.query(database.Metric).filter_by(name=metric_name).one()
    logging.debug('Got metric id = %d', metric.id)

    rows = []
    for snapshot in repository.snapshots:
        row = [snapshot.time]
        for name in file_set_names:
            file_set = dbs.query(database.FileSet
                    ).filter_by(snapshot=snapshot, name=name).one()
            logging.debug('Got file set id = %d', file_set.id)
            metric_value = dbs.query(database.FileSetMetricValue
                    ).filter_by(metric=metric, file_set=file_st).one()
            logging.debug('Got metric value id = %d', metric_value.id)
            row.append(metric_value.value)
        rows.append(row)

    logging.debug('Finsihed gathering metrics.')
    return rows

def save_metrics(data, file_set_names, filename):
    header = "# " + ",".join(file_set_names)
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def main(database_url, repository_name,
        metric_name, file_set_names, output_filename):
    logging.info('Starting tracer bullet report main.')
    database.initialize(database_url)
    data = gather_metrics(repository_name, metric_name, file_set_names)
    save_metrics(data, file_set_names, output_filename)
    logging.info('Ending tracer bullet report main.')

if '__main__' == __name__:
    args = parse_args()
    setup_logging(args.config)
    main(args.database_url, args.repository_name,
            args.metric_name, args.file_set_names, args.output_filename)
