# Brief:

The requirement needs to be developed in Python 3
Code should follow pep8 standards and should include pydoc, logging & unit tests
Please provide github link for review.

# Requirement:

- Download the xml from https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2020-01-08T00:00:00Z+TO+2020-01-08T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100
- From the xml, please parse through to the first download link whose file_type is DLTINS and download the zip
- Extract the xml from the zip.
- Convert the contents of the xml into a CSV with the following header:
- FinInstrmGnlAttrbts.Id
- FinInstrmGnlAttrbts.FullNm
- FinInstrmGnlAttrbts.ClssfctnTp
- FinInstrmGnlAttrbts.CmmdtyDerivInd
- FinInstrmGnlAttrbts.NtnlCcy
- Issr
- Store the csv from step 4) in an AWS S3 bucket
