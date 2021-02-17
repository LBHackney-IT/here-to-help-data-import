# Here to help: Data Ingestion
This tool is used to ingest and transform data from a google sheet into the here to [help help api](https://github.com/LBHackney-IT/cv-19-res-support-v3).

## Stack
- pytest test framework
- terraform to provision resources for the lambda

## How it works
This lambda is executed every 30min and looks for new spreadsheets in google drive.

Currently processing:
- Power BI spreadsheets that should be uploaded to `https://drive.google.com/drive/folders/CT_INBOUND_FOLDER_ID`
- National Shielding Service spreadsheet that should be uploaded to `https://drive.google.com/drive/folders/CEV_INBOUND_FOLDER_ID`

## Getting started

To create the virtual environment 
```bash
python3 -m venv venv
```
To activate the virtual envirment
```bash
. venv/bin/activate
```
To install pipenv (Mac OS)
```bash
brew install pipenv 
```

To install dependencies
```bash
pipenv install
```
To run tests
```bash
pytest
```
### Development
You can deploy to a development environment by committing to the development branch, for which there is an automated 
deployment process in CircleCI.
### Release process
We have an automated deployment process, which runs in CircleCI.

1. Automated tests (pytest) are run to ensure the release is of good quality.
2. The application is deployed to staging when changes are merged into the master branch.
5. We manually confirm a production deployment in the CircleCI workflow once we're happy with our changes in staging.
6. The application is deployed to production.

Our staging and production environments are hosted by AWS. We would deploy to production per each feature/config merged 
into  `master`  branch.
