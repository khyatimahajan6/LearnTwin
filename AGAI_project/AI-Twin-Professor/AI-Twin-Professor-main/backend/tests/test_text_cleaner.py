from utils.text_cleaner import clean_text

def test_clean_text_logic():
    input_text = """[Page 1]
1

Introduction to Databases


A database is a collection of related data
stored in a standard format.


Types of Data

1. Quantitative Data
2. Qualitative Data

● Numeric
● Alphanumeric
● Multimedia"""

    expected_output = """Introduction to Databases

A database is a collection of related data stored in a standard format.

Types of Data

1. Quantitative Data
2. Qualitative Data

- Numeric
- Alphanumeric
- Multimedia"""

    assert clean_text(input_text) == expected_output
