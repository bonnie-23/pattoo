"""Module that defines universal constants used only by pattoo.

The aim is to have a single location for constants that may be used across
agents to prevent the risk of duplication.

"""
# Standard imports
import collections

###############################################################################
# Constants for pattoo Web API
###############################################################################

PATTOO_INGESTER_SCRIPT = 'pattoo-ingester.py'
PATTOO_INGESTERD_NAME = 'pattoo-ingesterd'
PATTOO_API_WEB_NAME = 'pattoo-apid'
PATTOO_API_WEB_PROXY = '{}-gunicorn'.format(
    PATTOO_API_WEB_NAME)
PATTOO_API_AGENT_NAME = 'pattoo-api-agentd'
PATTOO_API_AGENT_PROXY = '{}-gunicorn'.format(
    PATTOO_API_AGENT_NAME)

###############################################################################
# Constants for data ingestion
###############################################################################

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_datapoint timestamp polling_interval value')

ChecksumLookup = collections.namedtuple(
    'ChecksumLookup', 'idx_datapoint last_timestamp polling_interval')
