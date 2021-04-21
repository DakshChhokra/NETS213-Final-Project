## Part 2.2: QC and Aggregation

### Raw Data Input

We take in the data from prior Reddit posts. In particular, we use a Kaggle dataset that used PRAW in 2020 to scrape the r/AmITheAsshole subreddit. Luckily, the r/AmITheAsshole contains a bot (the only bot that is allowed for the subreddit, since it has strict rules), that will classify the post given the four criteria (YTA, NTA, ESH, and NAH) as a tag for the post given the comments for the given post. WE use this data as the input for our criteria analysis, and the baseline for our comparison between crowdworkers and redditors. See: https://www.kaggle.com/spectrumpositive/praw-scrapings-from-ramitheasshole

Example Raw Data is found at: `/data/raw0207.csv`

### Aggregation Module
The aggregation module is comprised of HIT 1's questions which is the result from HIT 1. Once HIT 1 is complete, the questions must be aggregated together to develop the batch CSV for HIT 2. 

HIT 1 to HIT2 Aggregation

Big Idea: At a high level, this component takes id, AITA title, AITA body, three questions, one correct answer choice for each question, and two incorrect answer choices for each question. Then grouping each answer set (the three answer choices associated with each question), it stores them in a list. Then, the choices are randomly sorted through a randomizer. From here it displays the output. 

_Sample Input:_ `/src/` [EXPLANATION]

_Sample Output:_ `/src/` [EXPLANATION]

_Code:_ `/src/`

[EXPLAIN MORE HERE]

Post HIT 2 Aggregation

Big Idea: 

_Sample Input:_ `[PATH]` [EXPLANATION]

_Sample Output:_ `[PATH]` [EXPLANATION]

_Code:_ `[PATH]`
### Quality Control Module
This project employs a novel approach to Quality Control by using workers as the proxy for quality control. HIT 2 provides the actual information - HIT 1 in fact allows us to create targeted quality control (in essence, the crowd is checking the crowd). 

The purpose of HIT 1 is to create questions that are _validation_ questions for HIT 2. These validation questions are in the form of comprehension questions. Of course, blindly trusting workers to create questions may be problematic due to subjectivity. We reconcile this by checking if the worker correctly answers _at least one validation question_. This is because we cannot assume all questions are perfect, since there are no innate ways of performing quality control of workers creating questions. Since three independent workers are creating these questions, it seems reasonable that at least one question should be answerable, and thus we use the at least one criteria to reconcile this issue. 

Nevertheless, we also note that there is a situation where all three questions are too difficult. Recall, we use these questions to confirm if the worker reads the whole post. We don't want to simply throw away the response. Because of this, we perform a weighting instead of simply removing the HIT: HITs that answer at least one validation question are weighted with 1, and those where all validation questions are incorrect are weighted with 0.25.

We do this such that if there is a situation in which there is a tie, the lower weighted HIT may help break the tie. However, it cannot unduly influence the calculation due to our suspicion that they did not fully understand the post. 

Therefore, the actual quality control code is not overly complex - we use majority vote in addition to weighting. This is because the majority of the QC stems from HIT1, rather than some post-HIT analysis. 

_Sample Input:_ `/data/qc_sampleIn.csv`, `/data/qc_answersIn.csv` [Cleaned results from HIT 2, Answer Key generated from HIT 1 results]

_Sample Output:_ `/data/qc_outputWeight.csv` [Weights given response and answer from HIT 1]

_Code:_ `/src/qc.py`
## Part 2.1: Major components of Project

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
