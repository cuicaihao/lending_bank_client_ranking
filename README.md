# Case Study: Lending Bank Client Behaviour Prediction

==============================

## Project Background

Using machine learning, help the bank predict which clients are likely to subscribe to a new term deposit.

Lending Bank wants to attract term deposits to fund its lending business. In a term deposit, a client agrees to deposit funds and allow the bank to use them for a fixed length of time. In return, the bank will pay interest on the deposit.

The bank’s sales manager wants to market the product to their existing clients. 
They have historical information from a previous marketing campaign that includes client demographics, prior call experience, market conditions and the interest rate offered.

Using machine learning, help the bank predict which clients are likely to subscribe to a new term deposit. Explain how different features affect the decision.


## Problem

Perform an analysis of the given data to determine how different features are related to credit card eligibility. Build a machine learning model that can predict the subs_deposit.


## Data Schema
| NAME                  | DESCRIPTION                                                                                                                                          |
|---------------------- |----------------------------------------------------------------------------------------------------------------------------------------------------- |
| client_id             | unique ID of the client called [unique key]                                                                                                          |
| age_bracket           | age bracket of the contacted client (in years)                                                                                                       |
| job                   | job type of the contacted client                                                                                                                     |
| marital               | marital status of the contacted client                                                                                                               |
| education             | highest level of education done by the client                                                                                                        |
| has_housing_loan      | whether the client has a house loan                                                                                                                  |
| has_personal_loan     | whether the client has a personal loan                                                                                                               |
| prev_call_duration    | last contact duration (value = 0 if the client has not been contacted ever)                                                                          |
| contact_date          | date at which contact was made with the client (YYYY-MM-DD)                                                                                          |
| days_since_last_call  | number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)  |
| num_contacts_prev     | number of contacts performed before this campaign and for this client (numeric)                                                                      |
| poutcome              | outcome of the previous marketing campaign (categorical: "failure","nonexistent","success")                                                          |
| cpi                   | standing consumer price index before the call (monthly indicator)                                                                                    |
| subs_deposit          | Did the client subscribe to the term deposit? (binary: 1,0) [dependent variable]                                                                     |

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io



## Data Exploration

**'client_id'**
- client_id is a unique identifier for each client.
- No missing values.

**'age_bracket'**
- There are 4 categories of age brackets: ['18-24', '25-40', '41-60', '60+'].
- We can assume the other age brackets are not relevant to the marketing campaign.
- No missing values.

**'job'**

- There are 7 categories of job types: [ 'white-collar', 'other', 'technician','self-employed', 'blue-collar', 'pink-collar', 'entrepreneur'].
- No missing values.

**'marital'**
- There are 4 categories of marital status: ['married', 'single', 'divorced', 'unknown'].
- No missing values.

**'education'**

- There are 6 categories of education: ['bachelors', 'secondary', 'senior_secondary', 'masters', 'unknown', 'illiterate'].
- No missing values.

**'has_housing_loan'**
- There are 3 categories of housing loan: ['yes', 'no', 'unknown'].
- No missing values.
- half of the clients have a housing loan.

**'has_personal_loan'**
- There are 3 categories of personal loan: ['yes', 'no', 'unknown'].
- No missing values.
- About >80% of the clients have no personal loan.

**'prev_call_duration'**
- The duration of the previous call, 0 means the client has not been contacted before.
- No missing values.  
- <font color='red'> There maybe outliers in this feature </font>.
- The upper_bound is 956.0, about 93.6% of the clients have a previous call duration no more than 956 (seconds, aka, 16 mins).
- There are 98.025% of the clinets have a previous call duration less than 1400 (seconds, aka, 24 mins).
- 1.975% of the clients have a previous call duration more than 12000 (seconds, aka, 33 hours). <font color='red'> I doubt these values is 100 times larger of the 'real' values </font>
- <font color='red'>For example, client_id (21043) has a previous call duration of 180600s, which is 50.16 hours, but the actual duration is only 1806s, which is only 18 minutes.</font>


**'days_since_last_call'**
- The number of days that passed by after the client was last contacted from a previous campaignm, 999 means client was not previously contacted.
- No missing values.
- I think this 999 is quite confusing, because it can also means client has not been contacted 999 days with know the above definition.
- For modelling purpose, we can replace the 999 with a different value so that the values distribution is more uniform.
- About 3614 of 4000 clients is not previously contacted.
- We can create a new binary feature to indicate whether the client has been contacted before.

**'num_contacts_prev'**
- 3219 of the clients have 0 contacts.
- No missing values.
- This feature is related to 'days_since_last_last_call'.
- The value range is [0, 6].
- Only 1 client has been contacts 6 times, and the results is 'Success'.


**'poutcome'**
- There are 3 categories of previous marketing campaign outcome: ['failure', 'nonexistent', 'success'].
- No missing values.
- About 3219 of the 4000 clients have no previous results ['nonexistent'].
- <font color='red'> This feature need to compared with days_since_last_call </font>.


**'contact_date'**
- The date at which the client was contacted.
- No missing values.
- Raw Data format is dd/mm/yy.
- pandas will format the date to YYYY-mm-dd. 
- Only 50 uinique dates are present in the date.
- All the contact happend in the first 7 month of 2018 (Jan to July).
- The year, month, day of the month may not be veryhelpfull to distinguish the difference of the clients.
- The day of the week can be a good indicator of the time.


**'cpi'**
- standing consumer price index before the call (monthly indicator).
- No missing values.
- Base on the data, the CPI is usually between 50 and 100.
-  <font color='red'> There maybe outliers in this feature </font>.
- The upper_bound is 95.54, about 65 of the 4000 clients have a CPI > 100.
- I think these outliers are caused by the typo of the dot in digits.
- For example, clinet_id(33914) has a CPI of 95.54, but the actual CPI is 947.67, but maybe the real one is 94.67.
- We can not use this sample for prediction, but we can fix this in our modelling after we confirm that the typo is correct.

**'subs_deposit'**
- There are 2 categories (1/0) of term deposit subscription: ['yes', 'no'].


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
