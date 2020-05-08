# REST API

## The Assignment
The assignment can be divided in two parts, namely:
1. Create a (REST-ish) web service
2. Make a prediction on when a JIRA issue key is resolved

When the web service is started and accessed via http://127.0.0.1:5000,
the pages to visit are listed.
The first page listed (/api/issue/{issue-key}/resolve-fake) will show a fake hardcoded
resolution for issue key AVRO-1.

The second page listed (/api/issue/{issue-key}/resolve-prediction) will show when the
resolution date of an issue key, when the resolution date is known. If the issue-key is
not yet resolved, a prediction has been made on when the issue key will be resolved.

The third page listed (/api/release/{date}/resolved-since-now) will show the issues
that could be released together.

## Requirements

## install
```
pip install -r requirements.txt
```

## run web serice
```
python app.py
```

## When new data has been added:
  (1) Run Creating_DataFrame.ipynb
  (2) Run pipeline.ipynb
  (3) Run MachineLearningTrain
  (4) Run MachineLearningPredict

If all steps are completed succesfully data/results contains a file "prediction.csv".
This file contains the prediction made for each issue, and will be used in the
web service applicatoin.  
