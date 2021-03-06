#!/usr/bin/env python3
"""Administer the AgentXlate database table."""

from collections import namedtuple

# PIP3
from sqlalchemy import and_

# Pattoo PIP3 libraries
from pattoo_shared import log

# Import project libraries
from pattoo.db import db
from pattoo.db.models import AgentXlate, Language
from pattoo.db.table import language


def agent_xlate_exists(idx_language, key):
    """Get the db AgentXlate.idx_agent_xlate value for specific agent.

    Args:
        idx_language: Language table primary key
        key: Key for translation

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20128) as session:
        rows = session.query(AgentXlate.translation).filter(and_(
            AgentXlate.idx_language == idx_language,
            AgentXlate.agent_program == key.encode()
        ))

    # Return
    for _ in rows:
        result = True
        break
    return result


def insert_row(key, translation, idx_language):
    """Create a database AgentXlate.agent row.

    Args:
        key: AgentXlate key
        translation: AgentXlate translation
        idx_language: Language table index

    Returns:
        None

    """
    # Insert and get the new agent value
    with db.db_modify(20130, die=True) as session:
        session.add(
            AgentXlate(
                agent_program=str(key).strip().encode(),
                translation=str(translation).strip().encode(),
                idx_language=idx_language
            )
        )


def update_row(key, translation, idx_language):
    """Update a database AgentXlate.agent row.

    Args:
        key: AgentXlate key
        translation: AgentXlate translation
        idx_language: Language table index

    Returns:
        None

    """
    # Insert and get the new agent value
    with db.db_modify(20131, die=False) as session:
        session.query(AgentXlate).filter(and_(
            AgentXlate.agent_program == key.encode(),
            AgentXlate.idx_language == idx_language)).update(
                {'translation': translation.strip().encode()}
            )


def update(_df):
    """Import data into the .

    Args:
        _df: Pandas DataFrame with the following headings
            ['language', 'key', 'translation']

    Returns:
        None

    """
    # Initialize key variables
    languages = {}
    headings_expected = [
        'language', 'key', 'translation']
    headings_actual = []
    valid = True
    count = 0

    # Test columns
    for item in _df.columns:
        headings_actual.append(item)
    for item in headings_actual:
        if item not in headings_expected:
            valid = False
    if valid is False:
        log_message = ('''Imported data must have the following headings "{}"\
'''.format('", "'.join(headings_expected)))
        log.log2die(20082, log_message)

    # Process the DataFrame
    for _, row in _df.iterrows():
        # Initialize variables at the top of the loop
        count += 1
        code = row['language'].lower()
        key = str(row['key'])
        translation = str(row['translation'])

        # Store the idx_language value in a dictionary to improve speed
        idx_language = languages.get(code)
        if bool(idx_language) is False:
            idx_language = language.exists(code)
            if bool(idx_language) is True:
                languages[code] = idx_language
            else:
                log_message = ('''\
Language code "{}" on line {} of imported translation file not found during \
key-pair data importation. Please correct and try again. All other valid \
entries have been imported.\
'''.format(code, count))
                log.log2see(20041, log_message)
                continue

        # Update the database
        if agent_xlate_exists(idx_language, key) is True:
            # Update the record
            update_row(key, translation, idx_language)
        else:
            # Insert a new record
            insert_row(key, translation, idx_language)


def cli_show_dump():
    """Get entire content of the table.

    Args:
        None

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []
    rows = []
    Record = namedtuple('Record', 'language agent_program translation enabled')

    # Get the result
    with db.db_query(20137) as session:
        rows = session.query(Language)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20127) as session:
            line_items = session.query(
                Language.code,
                AgentXlate.enabled,
                AgentXlate.agent_program,
                AgentXlate.translation).filter(and_(
                    AgentXlate.idx_language == row.idx_language,
                    AgentXlate.idx_language == Language.idx_language)
                )

        if line_items.count() >= 1:
            # AgentXlates assigned to the group
            for line_item in line_items:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=line_item.enabled,
                            language=line_item.code.decode(),
                            agent_program=line_item.agent_program.decode(),
                            translation=line_item.translation.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            language='',
                            agent_program=line_item.agent_program.decode(),
                            translation=line_item.translation.decode()
                        )
                    )

        else:
            # Format only row for language
            result.append(
                Record(
                    enabled='',
                    language=row.code.decode(),
                    agent_program='',
                    translation=''
                )
            )

        # Add a spacer between language groups
        result.append(Record(
            enabled='', language='', agent_program='', translation=''))

    return result
