## Major components of Project

**Data Wrangling Phase (2 points)**



1. Collecting aggregated data from Kaggle Datasets that have been scrapped previously [https://www.reddit.com/r/AmItheAsshole/](https://www.reddit.com/r/AmItheAsshole/)
2. Cleaning the data based on a number of factors
    1. Controlling for the date of post
    2. Filtering posts that were updated or changed from original
    3. Controlling for sensitive and potentially disturbing content
    4. Controlling for the length of posts (some of them are too long/short)
3. Depending on if (2) reduces the number of posts substantially we will manually scrape Reddit for more content to feed into the next steps.

**Preparation & Output Data Pipeline of HIT 1 (4 points)**



1. Feed HIT1 the processed Kaggle Datasets
2. Develop HTML page that will be used by Turkers
    1. Designing the UI from the worker’s perspective and creating a seamless workflow
    2. Creating questions that they will need to answer for quality control
    3. Ensuring data connects to the HTML page
3. Testing to make sure the outlet functions are working properly
4. Publish HIT1 and wait for results
5. Feed HIT1 output data to HIT2

**Creation & Output of HIT 2 (4 points)**



1. Feed HIT2 the processed output of HIT1
2. Develop HTML page that will be used by Turkers
    1. Following similar steps to previous HIT creation, here we will create HIT 2 based on new UI and specifications to create an interactive and energetic page
3. Testing to make sure the outlet functions are working properly
4. Publish HIT2 and wait for results

**Analytics of MTurk Results (3 points)**



1. Collecting and aggregating data from HITs
2. Analyzing individual responses to develop consensus for each post
3. Creative way to display the posts based on results obtained

**Develop “Reddit Am I the Asshole” ML Predictor (5 points)**



1. This step will aim to create an automated predictor using NLP techniques to see if a batch of text would be flagged as “asshole” based on historical data
2. Data ingestion step
3. Data Preparation
    1. Normalization
    2. Transformation
    3. Validation
    4. Featurization
4. Model Building & Training
    5. Hyper-parameter tuning
    6. Model selection
    7. Model testing
    8. Model validation
5. Creation of ML Pipeline to predict a new body of text
