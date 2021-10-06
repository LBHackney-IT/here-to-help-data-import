# Introduction

The ingestion(s) take data from a Google Drive/sheet and send to the API, which is rendered in the front-end.

In order to investigate production issues and build features that span all projects, it can be useful to have a complete environment set up locally.

This document details setting up that environment.

# Getting started

1. Setup the Here To Help front-end following the [Readme](https://github.com/LBHackney-IT/coronavirus-here-to-help-frontend/blob/master/README.md)

2. Setup the Here to Help API following the [Readme] (https://github.com/LBHackney-IT/cv-19-res-support-v3/blob/master/README.md). Ensure all steps are followed to be able to run in Debug mode. If you run with make serve it will use the same port as the front-end and all three won't run together.

3. Change your local ingest .env CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL parameter to point to the local API, e.g: http://localhost:5000/api/

4. Change your .env INBOUND and OUTBOUND folder parameters to be a valid ID. This is the final portion of the path when accessing the folder in a browser:

e.g:

https://drive.google.com/drive/u/1/folders/1uq9_dtmTi_5cdA4Qj38BdUJHKbjQgxn7?ths=true

The ID is 1uq9_dtmTi_5cdA4Qj38BdUJHKbjQgxn7

5. Change lib_src\local_main.py to call the ingest type you wish to test.

6. Assuming the API and front-end are running debug mode. You can place a file in the relevant Google Drive inbound folder and run the ingest project in debug. You should be able to hit breakpoints on all three as the data traverses the system.

# Additional steps to setup your own Google Drive development folders and API key

Depending on what you have already, none or all of these will need to be followed:

1. Create a Google Drive folder, containing inbound / outbound. This should be a folder only accessible to you and not in a shared location.

2. In Google Cloud Platform, create a development project for yourself.

3. Enable the Drive API and Sheets API on your development project.

4. Create a service account in the development project with no roles and no access.

5. Generate a key and store it in \lib\key_file.json in the ingest project locally. This file is excluded from .gitignore but you should still ensure its a key with only access to your dev folders.

6. The service account listed in GCP will have an email address. Share the inbound and outbound folders with this email.


