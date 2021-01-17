#!/usr/bin/env python
# This is unit test case written to validate the count of records fetched after parsing the xml file to csv.
# To Test the result pytest has been used and screenshot capturing the validation has been uploaded.

def test_xml_parser():
    # reading the CSV file 
    row_count = sum(1 for line in open('Output_Data.csv',encoding="utf8"))
    assert row_count == 500001
        
