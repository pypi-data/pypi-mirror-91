import datetime


class MockDataType:
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name


# Mocked SQL query responses for test_metadata
table_names = {
    "data": [
        ("TEST_TABLE1", "T_DATA"),
        ("TEST_TABLE2", "T_DOCUMENT_DATA"),
        ("CUSTODY_HISTORY", "USERS"),
    ]
}
blob_list = {"data": [("TEST_TABLE1", "BLOB_COLUMN1"), ("TEST_TABLE2", "BLOB_COLUMN2")]}
primary_key = {"data": [("LONG_POSTCODE_ID",)]}
primary_keys = {"data": [("LONG_POSTCODE_ID",), ("TEAM_ID",)]}
partition_key = {
    "data": [
        (
            "TEST_SCHEMA",
            "TEST_TABLE",
            "TABLE",
            "PARTITION_KEY_A",
            1,
        )
    ]
}
partition_keys = {
    "data": [
        (
            "TEST_SCHEMA",
            "TEST_TABLE",
            "TABLE",
            "PARTITION_KEY_A",
            1,
        ),
        (
            "TEST_SCHEMA",
            "TEST_TABLE",
            "TABLE",
            "PARTITION_KEY_B",
            1,
        ),
        (
            "TEST_SCHEMA",
            "TEST_TABLE",
            "TABLE",
            "PARTITION_KEY_C",
            1,
        ),
    ]
}
first_table = {
    "desc": [
        ("TEST_NUMBER", MockDataType("DB_TYPE_NUMBER"), 39, None, 38, 0, 1),
        ("TEST_ID", MockDataType("DB_TYPE_NUMBER"), 127, None, 0, -127, 1),
        ("TEST_DATE", MockDataType("DB_TYPE_DATE"), 23, None, None, None, 1),
        ("TEST_VARCHAR", MockDataType("DB_TYPE_VARCHAR"), 30, 30, None, None, 1),
        ("TEST_FLAG", MockDataType("DB_TYPE_VARCHAR"), 1, 1, None, None, 1),
        ("TEST_RAW", MockDataType("DB_TYPE_RAW"), 8, 8, None, None, 1),
        ("TEST_ROWID_SKIP", MockDataType("DB_TYPE_ROWID"), 127, None, 0, -127, 1),
        ("TEST_OBJECT_SKIP", MockDataType("DB_TYPE_OBJECT"), 127, None, 0, -127, 1),
        ("TEST_BLOB_SKIP", MockDataType("DB_TYPE_BLOB"), 127, None, 0, -127, 1),
    ],
    "data": [
        (
            63495,
            7833,
            datetime.datetime(2020, 6, 23, 10, 39, 12),
            "INSTITUTIONAL_REPORT_TRANSFER",
            "I",
            b"bc512911a3ce8e1f",
            12345678,
            "OBJECT",
            "BLOB",
        )
    ],
}
second_table = {
    "desc": [
        ("SPG_ERROR_ID", MockDataType("DB_TYPE_NUMBER"), 39, None, 38, 0, 1),
        ("ERROR_DATE", MockDataType("DB_TYPE_DATE"), 23, None, None, None, 1),
        ("MESSAGE_CRN", MockDataType("DB_TYPE_CHAR"), 7, 7, None, None, 1),
        ("NOTES", MockDataType("DB_TYPE_CLOB"), None, None, None, None, 1),
        ("INCIDENT_ID", MockDataType("DB_TYPE_VARCHAR"), 100, 100, None, None, 1),
        ("TEST_BLOB_SKIP", MockDataType("DB_TYPE_BLOB"), 127, None, 0, -127, 1),
    ],
    "data": [
        (
            198984,
            datetime.datetime(2018, 8, 2, 14, 49, 21),
            "E160306",
            "CLOB TEXT",
            1500148234,
            "BLOB",
        )
    ],
}
empty_table = {
    "description": [
        ("TEST_NUMBER", MockDataType("DB_TYPE_NUMBER"), 39, None, 38, 0, 1),
        ("TEST_ID", MockDataType("DB_TYPE_NUMBER"), 127, None, 0, -127, 1),
        ("TEST_DATE", MockDataType("DB_TYPE_DATE"), 23, None, None, None, 1),
        ("TEST_VARCHAR", MockDataType("DB_TYPE_VARCHAR"), 30, 30, None, None, 1),
        ("TEST_FLAG", MockDataType("DB_TYPE_VARCHAR"), 1, 1, None, None, 1),
        ("TEST_ROWID_SKIP", MockDataType("DB_TYPE_ROWID"), 127, None, 0, -127, 1),
        ("TEST_OBJECT_SKIP", MockDataType("DB_TYPE_OBJECT"), 127, None, 0, -127, 1),
        ("TEST_BLOB_SKIP", MockDataType("DB_TYPE_BLOB"), 127, None, 0, -127, 1),
    ]
}
doc_history = {
    "desc": [("TEST_ID", MockDataType("DB_TYPE_NUMBER"), 127, None, 0, -127, 1)],
}
test_constraints = {
    "desc": [],
    "data": [
        ("TEST_TABLE1", "TEST_NUMBER", "C", "'TEST_NUMBER' IS NOT NULL"),
        ("TEST_TABLE1", "TEST_ID", "P", ""),
        ("TEST_TABLE1", "TEST_DATE", "C", "SOMETHING ELSE"),
        ("TEST_TABLE2", "MESSAGE_CRN", "C", "'TEST_FLAG' IS NOT NULL"),
        ("TEST_TABLE2", "INCIDENT_ID", "P", ""),
        ("TEST_TABLE2", "NOTES", "C", "SOMETHING ELSE"),
        ("TABLE_NOT_PRESENT", "NO_DATA", "P", ""),
    ],
}
