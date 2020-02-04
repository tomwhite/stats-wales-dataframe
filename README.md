[StatsWales](https://statswales.gov.wales/Catalogue) provides all kinds of useful and interesting public data,
however it can be awkward to download it manually and process it with tools like R and Python, due to the way it handles
hierarchical categories.

This repository has a simple command line tool to download StatsWales data in CSV format for easy processing in
R and Python.

The tool uses Python to run, but you can use any language to do downstream analysis of the data.

### Installation

Create a Python virtual environment to run in:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage

On the [StatsWales website](https://statswales.gov.wales/Catalogue) find the dataset that you are interested in.

For example, [Population estimates by local authority and year](https://statswales.gov.wales/Catalogue/Population-and-Migration/Population/Estimates/Local-Authority/populationestimates-by-localauthority-year).

In the "Metadata" section at the end of the page, under the "Open Data" tab, there are a number of URLs.

The 'Items' URL allows you to find information about the data dimensions and valid values for each dimension.
This is useful for filtering the datasets.

The following downloads the items information for the population dataset and saves it in a local CSV file in _/tmp/popu0003_items.csv_.

```bash
python tocsv.py /tmp/popu0003_items.csv 'http://open.statswales.gov.wales/en-gb/discover/datasetdimensionitems?$filter=Dataset%20eq%20%27popu0003%27'
```

If we look in the CSV file we can find codes for _All ages_ and _Persons_ (since we want to roll up by these
dimensions, that is not have a fine-grained breakdown by age and gender).

Then we can download the actual dataset data with the following. The filter specifies all ages and genders.
Since no area or year filters are specified, data will be broken down for each area and year.

```bash
python tocsv.py /tmp/popu0003_all.csv http://open.statswales.gov.wales/en-gb/dataset/popu0003 "Age_Code eq '0099' and Gender_Code eq 'P'"
```

The general usage is

```
python tocsv.py <csv_file> <stats_wales_url> [optional_filter]
```
