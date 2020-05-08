# REST API

## Assignment
The assignment can be divided in two parts, namely:
1. Create a (REST-ish) web service
2. Make a prediction on when a JIRA issue key is resolved

When the web service is started and accessed via http://127.0.0.1:5000, the pages to visit are listed.

* The first page listed (/api/issue/{issue-key}/resolve-fake) will show a fake hardcoded
resolution for issue key AVRO-1.
* The second page listed (/api/issue/{issue-key}/resolve-prediction) will show the
resolution date of an issue key, when the resolution date is known. If the issue-key is
not yet resolved, a prediction has been made on when the issue key will be resolved.
* The third page listed (/api/release/{date}/resolved-since-now) will show the issues
that could be released together.

## Notebooks

* Creating_Dataframe.ipynb: Extracts and creates features from the original datasets (avro_issue, avro_daycount, avro_transactions) that will be used in the exploratory data analysis and prediction. 
* pipeline.ipynb: Runs the data created in *creating_dataframe* through a pipeline. By doing so the data has been cleaned for the machine learning algorithm
* MachineLearningTrain.ipynb: Data that has been transformed by *pipeline* will be used to train the machine learning algorithm. Only those issues will be used that have a resolved date. 
* MachineLearningPredict.ipynb: The machine learning algorithm that has been created in *MachineLearningTrain* will be used to make a prediciton on all issues. Results will be stored in the data/result folder.

## Requirements

### Install
```
pip install -r requirements.txt
```

### Run web service
```
python app.py
```

## New data:

When data has been removed or changed, in order for this data to be used the following steps have to be taken:

 1. Run Creating_DataFrame.ipynb
 2. Run pipeline.ipynb
 3. Run MachineLearningTrain.ipynb
 4. Run MachineLearningPredict.ipynb

If all steps are completed succesfully the folder data/results contains a file *prediction.csv*.
This file contains the prediction made for each issue, and will be used in the web service application.  
