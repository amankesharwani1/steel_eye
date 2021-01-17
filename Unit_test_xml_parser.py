import csv
def test_xml_parser():
    # reading the CSV file 
    row_count = sum(1 for line in open('Output_Data.csv',encoding="utf8"))
    assert row_count == 500001
        