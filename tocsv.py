import os.path
import pandas as pd
import requests
import sys

# inspired by https://github.com/nismod/ukpopulation/blob/master/ukpopulation/snppdata.py#L256

# Examples
#
# Load item metadata
# python tocsv.py /tmp/popu0003_items.csv 'http://open.statswales.gov.wales/en-gb/discover/datasetdimensionitems?$filter=Dataset%20eq%20%27popu0003%27'
#
# Filtering
# python tocsv.py /tmp/popu0003_all.csv http://open.statswales.gov.wales/en-gb/dataset/popu0003 "Age_Code eq '0099' and Gender_Code eq 'P'"
# python tocsv.py /tmp/popu0003_0-15.csv http://open.statswales.gov.wales/en-gb/dataset/popu0003 "Age_Code eq '0015' and Gender_Code eq 'P'"
# python tocsv.py /tmp/popu0003_16-64.csv http://open.statswales.gov.wales/en-gb/dataset/popu0003 "Age_Code eq '1664' and Gender_Code eq 'P'"
# python tocsv.py /tmp/popu0003_64_and_over.csv http://open.statswales.gov.wales/en-gb/dataset/popu0003 "Age_Code eq '6599' and Gender_Code eq 'P'"

def read_odata(csv_file, url):
    data = []
    while True:
        print(url)
        r = requests.get(url)
        r_data = r.json()
        data += r_data['value']
        if "odata.nextLink" in r_data:
            url = r_data["odata.nextLink"]
        else:
            break

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    df.to_pickle("./df.pkl")
    return df

if __name__ == '__main__':
    csv_file = sys.argv[1]
    url = sys.argv[2]
    if len(sys.argv) >= 4:
        url += "?&$filter={}".format(sys.argv[3])

    df = read_odata(csv_file, url)

    pd.set_option('display.max_columns', None)
    print(df.columns)
    print(df)
