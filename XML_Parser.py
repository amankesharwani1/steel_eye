#!/usr/bin/env python
# coding: utf-8

#-----------------------------------------------------------------------------
# This example will read an XML file and parse out the data using the
# lxml.etree library that is included in the standard library. 
# There are a number of external XML parsing libraries that can be used with 
# Python. Details are available at wiki.python.org/moin/PythonXml. If you plan 
# to do a lot of XML processing, then I would suggest looking at the lxml 
# library. It is based on libxml2 and libxslt and is fast and easy to use. You 
# can get more information about lxml at http://lxml.de/index.html. 
#-----------------------------------------------------------------------------


# In[21]:


#Import the necessary python libraries.

from lxml import etree
import unicodecsv as csv
import codecs
import time
import logging
import traceback


# In[22]:


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# In[32]:


def xml_parser(file_name):
    logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(asctime)s %(levelname)s:%(message)s')
    start_time = time.time()

    # Strip the namespaces from the tags
    def strip_tag_name(t):
        t=elem.tag
        idx = k = t.rfind("}")
        if idx!=-1:
            t = t[idx +1:]
        return t
    try:
        # Create an output csv file for writing the extracted content from the xml file
        f = open('Output_Data.csv', 'wb')

        # create the csv writer object
        csvwriter = csv.writer(f, dialect='excel', encoding = 'utf-8')

        # Create the list of column names and write it to csv file. This is the header line.
        col_names=['Id','FullNm','ClssfctnTp','CmmdtyDerivInd','NtnlCcy', 'Issr']
        csvwriter.writerow(col_names)
        logging.debug("Empty file with file name Output_Data.csv has been created")
        
    except OSError as e:
        logging.error("Error creating the file")

            

    try:
        # Read the file
        from lxml import etree

        context = etree.iterparse(file_name, events=('start','end'))
        logging.debug("XML file with name {0} read successfully".format(file_name))
    
    except OSError as e:
        logging.error("File with name {0} not found".format(file_name))

    try:
    
        # Process all of the start/end tags and obtain the tanme of each tag
        tcount=0
        Issr=''
        for event,elem in context:
            tname = strip_tag_name(elem.tag)
            
            if event == 'start':
                
                if tname == 'FinInstrmGnlAttrbts':
                    Id = ''
                    FullNm = ''
                    ClssfctnTp = ''
                    CmmdtyDerivInd = ''
                    NtnlCcy = ''
            
                elif tname == 'Id':
                    Id=elem.text
                elif tname == 'FullNm':
                    FullNm = elem.text
                elif tname == 'ClssfctnTp':
                    ClssfctnTp=elem.text
                elif tname == 'CmmdtyDerivInd':
                    CmmdtyDerivInd=elem.text
                elif tname == 'NtnlCcy':
                    NtnlCcy=elem.text
                elif tname == 'Issr':
                    Issr=elem.text
                
            elif tname == 'FinInstrmGnlAttrbts':
                tcount += 1
                #if tcount > 1 and (tcount % 100000) == 0:
                #    print("{:,}".format(tcount))

                csvwriter.writerow([Id, FullNm, ClssfctnTp, CmmdtyDerivInd, NtnlCcy, Issr])


            elem.clear() 
        
        logging.debug("Total records read from XML and written to CSV file are {0}".format(tcount))

    except:
        logging.error("uncaught exception: %s", traceback.format_exc())

    
    time_took = time.time() - start_time
    logging.debug(f"Total runtime: {hms_string(time_took)}")    


# In[33]:


xml_parser("DLTINS_20200108_01of03.xml")


# In[ ]:

#### Upload the CSV file to S3 bucket
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('Output_Data.csv', 'bucket_name', 's3_file_name')

