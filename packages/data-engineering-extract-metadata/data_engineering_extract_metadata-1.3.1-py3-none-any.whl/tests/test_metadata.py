import os
import tests.mocked_responses as mocks

from pathlib import Path
from tests import MockConnection, MockCursor
from data_engineering_extract_metadata.utils import read_json
from data_engineering_extract_metadata.metadata import (
    create_json_for_database,
    create_json_for_tables,
    get_table_meta,
    get_primary_keys,
    get_partition_keys,
    find_not_nullable,
)

test_path = Path("./tests/data")
expected_path = Path("./tests/expected_data")


def test_create_json_for_database():
    """Tests json file is created with correct content"""
    try:
        create_json_for_database(
            "This is a database",
            "test_database",
            "bucket-name",
            "hmpps/delius/DELIUS_APP_SCHEMA",
            test_path,
        )
        output = read_json("database.json", test_path)
    finally:
        os.remove(test_path / "database.json")

    expected = read_json("database_expected.json", expected_path)

    assert output == expected


def test_create_json_for_tables():
    """Tests that the correct json is created for multiple tables"""
    # List of query responses. Empty dicts are for primary key & partition queries
    responses = [
        mocks.test_constraints,
        mocks.first_table,
        {},
        {},
        mocks.second_table,
        {},
        {},
    ]
    try:
        create_json_for_tables(
            tables=["TEST_TABLE1", "TEST_TABLE2"],
            schema="TEST_DB",
            location=test_path,
            include_op_column=True,
            include_timestamp_column=True,
            include_derived_columns=False,
            include_objects=False,
            connection=MockConnection(responses),
        )
        output1 = read_json("test_table1.json", test_path)
        output2 = read_json("test_table2.json", test_path)

    finally:
        os.remove(test_path / "test_table1.json")
        os.remove(test_path / "test_table2.json")

    expected1 = read_json("table1_expected.json", expected_path)
    expected2 = read_json("table2_expected.json", expected_path)

    assert output1 == expected1
    assert output2 == expected2


def test_get_table_meta():
    """Tests option flags, document_history tables and data type conversion
    Primary key fields tested separately

    This function receives a cursor that's already had .execute run
    This means it should already have a description and data if needed

    That's why MockCursors used here are initialised with the description parameter
    """
    # All flag parameters set to False
    output_no_flags = get_table_meta(
        MockCursor(description=mocks.first_table["desc"]),
        table="TEST_TABLE1",
        schema="TEST_SCHEMA",
        not_nullable=["test_id", "test_number"],
        include_op_column=False,
        include_timestamp_column=False,
        include_derived_columns=False,
        include_objects=False,
    )
    columns_no_flags = [
        {
            "name": "test_number",
            "type": "decimal(38,0)",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_date",
            "type": "datetime",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_varchar",
            "type": "character",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_flag",
            "type": "character",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_raw",
            "type": "binary",
            "description": "",
            "nullable": True,
        },
    ]
    expected_no_flags = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "test_table1",
        "description": "",
        "data_format": "parquet",
        "columns": columns_no_flags,
        "location": "TEST_TABLE1/",
        "partitions": None,
        "primary_key": None,
    }

    # All parameter flags set to True
    output_all_flags = get_table_meta(
        MockCursor(description=mocks.first_table["desc"]),
        table="TEST_TABLE1",
        schema="TEST_SCHEMA",
        not_nullable=["test_flag", "test_varchar"],
        include_op_column=True,
        include_timestamp_column=True,
        include_derived_columns=True,
        include_objects=True,
    )
    columns_all_flags = [
        {
            "name": "op",
            "type": "character",
            "description": "Type of change, for rows added by ongoing replication.",
            "nullable": True,
            "enum": ["I", "U", "D"],
        },
        {
            "name": "extraction_timestamp",
            "type": "datetime",
            "description": "DMS extraction timestamp",
            "nullable": False,
        },
        {
            "name": "test_number",
            "type": "decimal(38,0)",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_date",
            "type": "datetime",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_varchar",
            "type": "character",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_flag",
            "type": "character",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_raw",
            "type": "binary",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_object_skip",
            "type": "array<character>",
            "description": "",
            "nullable": True,
        },
        {
            "name": "mojap_current_record",
            "type": "boolean",
            "description": "If the record is current",
            "nullable": False,
        },
        {
            "name": "mojap_start_datetime",
            "type": "datetime",
            "description": "When the record became current",
            "nullable": False,
        },
        {
            "name": "mojap_end_datetime",
            "type": "datetime",
            "description": "When the record ceased to be current",
            "nullable": False,
        },
    ]
    expected_all_flags = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "test_table1",
        "description": "",
        "data_format": "parquet",
        "columns": columns_all_flags,
        "location": "TEST_TABLE1/",
        "partitions": None,
        "primary_key": None,
    }

    # DOCUMENT_HISTORY table
    output_doc_history = get_table_meta(
        MockCursor(description=mocks.doc_history["desc"]),
        table="DOCUMENT_HISTORY",
        schema="TEST_SCHEMA",
        not_nullable=[],
        include_op_column=False,
        include_timestamp_column=False,
        include_derived_columns=False,
        include_objects=False,
    )
    columns_doc_history = [
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": True,
        },
    ]
    expected_doc_history = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "document_history",
        "description": "",
        "data_format": "parquet",
        "columns": columns_doc_history,
        "location": "DOCUMENT_HISTORY/",
        "partitions": None,
        "primary_key": None,
    }

    assert output_no_flags == expected_no_flags
    assert output_all_flags == expected_all_flags
    assert output_doc_history == expected_doc_history


def test_get_primary_keys():
    """Tests that primary key output is formatted correctly
    Doesn't check that the SQL results are right
    """
    output_key = get_primary_keys("TEST_TABLE_KEY", MockCursor([mocks.primary_key]))
    output_keys = get_primary_keys("TEST_TABLE_KEYS", MockCursor([mocks.primary_keys]))
    output_no_keys = get_primary_keys("TEST_TABLE_NO_KEYS", MockCursor())

    expected_key = [
        "long_postcode_id",
    ]
    expected_keys = ["long_postcode_id", "team_id"]
    expected_no_keys = None

    assert output_key == expected_key
    assert output_keys == expected_keys
    assert output_no_keys == expected_no_keys


def test_get_partition_keys():
    """Tests that partition keys are returned correctly"""
    output_key = get_partition_keys(
        schema="TEST_SCHEMA",
        table="TEST_TABLE",
        cursor=MockCursor([mocks.partition_key]),
    )
    output_keys = get_partition_keys(
        schema="TEST_SCHEMA",
        table="TEST_TABLE",
        cursor=MockCursor([mocks.partition_keys]),
    )
    output_no_keys = get_partition_keys(
        schema="TEST_SCHEMA",
        table="TEST_TABLE",
        cursor=MockCursor(),
    )

    expected_key = ["partition_key_a"]
    expected_keys = [
        "partition_key_a",
        "partition_key_b",
        "partition_key_c",
    ]
    expected_no_keys = None

    assert output_key == expected_key
    assert output_keys == expected_keys
    assert output_no_keys == expected_no_keys


def test_find_not_nullable():
    output = find_not_nullable(MockCursor([mocks.test_constraints]), "TEST_SCHEMA")
    assert output == {
        "test_table1": ["test_number", "test_id"],
        "test_table2": ["message_crn", "incident_id"],
        "table_not_present": ["no_data"],
    }
