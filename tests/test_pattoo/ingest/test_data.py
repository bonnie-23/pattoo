#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data as lib_data
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import pair, datapoint
from pattoo.ingest import get
from pattoo.ingest import data as ingest_data


class TestExceptionWrapper(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_re_raise(self):
        """Testing method / function re_raise."""
        pass


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_mulitiprocess(self):
        """Testing method / function mulitiprocess."""
        pass

    def test__process_rows(self):
        """Testing method / function _process_rows."""
        pass

    def test_process_db_records(self):
        """Testing method / function process_db_records."""
        # Initialize key variables
        checksum = lib_data.hashstring(str(random()))
        agent_id = lib_data.hashstring(str(random()))
        data_type = DATA_FLOAT
        polling_interval = 10 * 1000
        pattoo_key = lib_data.hashstring(str(random()))
        _timestamp = int(time.time() * 1000)
        expected = []
        timestamps = []
        records = []

        # Create a list of PattooDBrecord objects
        for pattoo_value in range(0, 5):
            timestamp = _timestamp + (pattoo_value * polling_interval)
            expected.append({'timestamp': _timestamp, 'value': pattoo_value})
            timestamps.append(timestamp)
            record = PattooDBrecord(
                pattoo_checksum=checksum,
                pattoo_key=pattoo_key,
                pattoo_agent_id=agent_id,
                pattoo_agent_polling_interval=polling_interval,
                pattoo_timestamp=timestamp,
                pattoo_data_type=data_type,
                pattoo_value=pattoo_value,
                pattoo_agent_polled_target='pattoo_agent_polled_target',
                pattoo_agent_program='pattoo_agent_program',
                pattoo_agent_hostname='pattoo_agent_hostname',
                pattoo_metadata=[]
            )
            records.append(record)

        # Create key-pair values in the database
        kvps = get.key_value_pairs(records)
        pair.insert_rows(kvps)

        # Insert
        ingest_data.process_db_records(records)

        # Get data from database
        idx_datapoint = datapoint.checksum_exists(checksum)
        _dp = datapoint.DataPoint(idx_datapoint)
        ts_start = min(timestamps)
        ts_stop = max(timestamps)
        result = _dp.data(ts_start, ts_stop)

        # Test
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
