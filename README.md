# What is the Data ingestion process?

The data ingestion process is a process which ingests data from a Google sheet into the here-to-help database through the [help help api](https://github.com/LBHackney-IT/cv-19-res-support-v3).

There are three data ingestion processes, and therefore three lambdas in this single repository:

- Here to Help data ingestion lambda - ingests contact tracing data into the here to help API
- Here to Help data ingestion NSSS lambda - ingests national shielding service data into the Here to Help API
- Here to Help data ingestion SPL lambda- ingests shielding patient list data into the Here to Help API

# Stack

- All AWS resources are provisioned using terraform
- Lambdas run on a python runtime environment as this is the preferred language for the data ingestion team
- We are using CircleCI for our CI/CD process
- pytest test framework

# How it works
![](https://user-images.githubusercontent.com/46002877/110338795-526abb00-801f-11eb-94c7-abc6d0d19d5b.png)

- AWS Lambdas have a maximum execution time of 15 minutes. Therefore, the ingestion lambda is configured to invoked by a cloudwatch event every 16 mins, this is to avoid concurrency issues

- To ingest the data, there is a manual task which requires a file to be uploaded to a Google Drive which the relevant lambda function will process

- The file must be uploaded to the relevant folder to be picked up by the correct lambda function:

  - For contact tracing data, navigate to inbound and upload the file there https://drive.google.com/drive/folders/CT_INBOUND_FOLDER_ID
  - For NSSS data, navigate to cev-nss, inbound and upload the file there
    https://drive.google.com/drive/folders/CEV_INBOUND_FOLDER_ID
  - For SPL data, navigate to cev-spl, inbound and upload the file there
    https://drive.google.com/drive/folders/SPL_INBOUND_FOLDER_ID

- The lambda reads the uploaded file, then one record at a time calls the here to help api
- The here to help api checks if the resident already exists in the database and adds them if they do not
  - For contact tracing, the here to help api only adds records if there is no help request with the same ctas id
  - For NSS, the here to help api only adds records if there is no help request with the nss id. It adds a case note if the NSS details have changed
  - For SPL, the here to help api only adds records if there is no help request with the spl id. It adds a case note if the SPL details have changed
  - The lambdas send the nss id and spl id as metadata whilst making the request to the here to help api
- The lambda will only process files uploaded on that day
- A limit of 3000 residents/rows has been agreed as the lambda could time out beyond this (if it takes longer than the 15 min timeout period set on the lambda to process the entire file)
- If there are more than 3000 residents, you can split the data into multiple files which will process consecutively (this only applies for SPL and NSSS, if you would like to upload more than 3000 contact tracing residents, please read further for guidance)
- Once a file has been processed, the lambda will upload a file in the outbound folder summarising all the processed residents

- The lambda only processes non-processed files. It identifies non-processed files differently for the three lambdas:

  - For contact tracing lambda, we only expect a single file to be uploaded per day, therefore the lambda only processes a single file uploaded on that day. If you would like to upload another file on the same day, then make sure to remove the file that was generated in the outbound folder. This is because it checks the creation date of the file in the outbound folder to see if a file had been processed on that day
  - For the SPL and NSSS lambda, the lambdas can process multiple files. It will process files that do not have a corresponding outbound file(compares names and dates of files), but it will only do so if the number of files in the inbound and outbound folders are not the same. This is because the lambda checks the file counts to verify that the inbound files have been processed. Ensure that you do not have multiple files with the same name on the same day so each file is processed
  - You should not manually add files to the outbound folder as this could break the process. If you would like to delete an outbound file ensure to delete the respective inbound file first to avoid reprocessing. For this reason, you should not remove files from the outbound folder
    You can verify that the ingestion process has run by navigating to the resident profile in Here to Help (staging, production) and checking that an ingestion case note is created

- In the case that this fails, please refer to the error handling guidance below

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
3. We manually confirm a production deployment in the CircleCI workflow once we're happy with our changes in staging.
4. The application is deployed to production.

Our staging and production environments are hosted by AWS. We would deploy to production per each feature/config merged
into `master` branch.

# Handling errors

## Common errors

- Uploaded spreadsheet does not have the correct headers
- Dates of birth are not formatted correctly in the spreadsheet, they should be in a standard date format (they are not the same for the three ingestion types- see example files)
- The lambdas time out, this is because they are processing files that are too large and go beyond the 15 min lambda execution time

## Error notifications

- In the case that one of the lambdas logs an error in the AWS CloudWatch logs, an email would be sent to a specific list of recipients (currently Huu Do, Christopher Caden andBen Dalton)
- To update this list, you need to set the recipients(ensuring each email is comma separated) on an AWS parameter store, this is stored under:

  `/here-to-help-data-ingestion/staging/email-addresses-for-sns`

  Once this is updated, the lambda should be redeployed (see deployment process above) and email will be sent to confirm subscription

- You can now see the time at which the lambda failed and track the relevant log stream on CloudWatch to investigate further
  The alarm does not specify which lambda has failed so checking the time and comparing against each of the logs will be necessary
