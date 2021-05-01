# r/IsSociety Screwed

NETS 213 Final Project, 2021A

Daniel Ng, Anish Bathwal, Daksh Chokra, Vaibhaw Ladha, Gund Jungsanguanpornsuk
## Part 3: HIT Design and System Integration Checkpoint

We have successfully completed the "bones" of the project. The next steps include actually submitting the HITs into the world, running the necessary code, and generating results. 

### HIT Design

The HIT design used for both HITs are in `/mturk_htmls`. There are two HTMLs. `comprehension_html.html` and `validator_html.html`. 

#### Comprehension HTML
Comprehension HTML, which is now currently live on MTurk Workshop, has the posts for people to create validation questions. Currently it is populated with actual posts that we will indeed use. 

This HTML uses Amazon's crowd APIs to create the HIT. It has a simple 4 boxes for turkers to enter a question, and correct/incorrect answers. 

#### Validator HTML
Taking in the questions from the Comprehension HTML (HIT 1), Validation HTML (HIT 2) feeds these questions and answers into a new batch. **Please note that the current HIT uses dummy text from an input dummy CSV** (`/AITA_Validator.csv`). This is because we do not yet have the questions to the posts yet. 

We have incorporated the TA's advice and now include a field for people to input that an answer is incorrect. They can now explain why. 

#### Discussion on Analysis Planned
We plan to do 2 analysis, as discussed at the beginning of this project. 

(1) Compare AITA? between Redditers and MTurkers. We want to see if there is a discernible difference in how MTurkers judge people. In particular, one can think of Reddit as a crowdsourcing method, where the best comments are upvoted. However, Reddit is a social network that is likely to have a certain bias. We thus compare this with mturkers, which seem to have a larger reach. This is fairly simple to implement, as we already have the equivalent of the groundtruth of the redditers in the subset. WE just simply need to compare the posts between the Mturkers and Reddit, since we have restricted the posts that are in the HITs to only be those which we have Reddit results. We will perform standard EDA and generate some insights. 

(2) Create ML models. We will create two seperate models: one using the crowdsourced labels, and then another using the original Reddit labels. We will use this to determine if there is a difference on a brand new post, but more importantly, allow us to attain some judgement a la wisdom of the crowds. This will be done primarily using NLP models to generate a model that can predict these crowds. Of course, we note that this may be challenging given the wide ranging posts, but we believe that there may be trends that cause judgement, and we want to use these models to determine if we can in fact reasonably estimate. 

##### Drawbacks of Analysis

We know that the analyzing how crowds are making predictions is near impossible - we are doing an experiment on something judgemental. Because of this, we note that the best data we have to groundtruth is Reddit. 

Further, we note that this method is unlikely to scale due to the cost of getting these HITs out. However, we believe that this could be an interesting experiment that could later be replicated in a game setting without funds. 
### System Flow

#### Data Wrangling: (2 pts) DONE
We have completed the Data Wrangling phase of the project. In particular, we clean the data based on a few factors: 
  - We remove non ASCII characters allowed by Reddit but not MTurk. 
  - We combine all posts in the dataset, and eliminate duplicate submissions. 
  - We ignore general Moderator posts such as new updates to the forum
  - We ignore any posts that are updates to prior posts, as they typically do not contain true judgemental discussion. 
  - We remove abnormal spacing typically found in Reddit to chunk posts, as this causes issues with MTurk and multiline strings. 

This gets us to roughly 900 posts. We note that these posts are actually quite abnormally skewed to NTA. However, to provide a reasonable sample, we collate 300 posts based on a mix of different tags. 
   - Note: These tags are generated based on a reddit bot that is the only permitted bot on the subreddit. It takes the top comments, identify the rating, and then determine the decision after 48 hours. Note that the subreddit is designed to be in contest mode for the first hour, so this allows for the best comment to truly be the best comment and then traction continues the trend. In essence, Reddit is its own crowdsource. 

   We split the dataset as following: The full 900 posts will be used in our ML predictor for Redditers. The curated 300 is then used to feed into the HITs. 

This is found in `src/GeneratePostCorpus.ipnyb`. The Source HIT corpus for crowdsourcing is under `data/HITCorpus.csv`. The entire cleaned dataset is called `data/cleanedDataset.csv`

#### Preparation and Output Data Pipeline of HIT 1: (4pts) SETUP DONE

The above code has prepared the data for input to HIT1. We just need to wait for the results. 

The HTML page for HIT 1 is discussed above.

An example for HIT 1 is published in the sandbox, and we plan to release it out to the world in the coming days. 

Then the results from HIT 1 will be processed by our aggregation modules discussed below. In further detail, the results that come from HIT 1 are then fed to `aggregation_comprehension.py`. Since each HIT is only one question (this is designed intentionally so that different people create different questions in hopes to reduce bias and confusion), this aggregates the responses from HIT 1 into the single line needed for HIT 2. This thus creates all three questions associated to the same post ID. Then afterwards, it shuffles the answer choices and provides us the correct answer choice in the csv. 



### Creation and Output Of HIT 2: (4pts) SETUP DONE

We take the result from the above file and then feed this into HIT 2. Please see above for discussion on HIT 2. 

After this is processed, this result from HIT 2 is then feeded into our Quality Control module. This is found in `qc.py`. In particular, this takes the results of the HITs and compares them to their answers. We check to see the accuracy of the questions. Please see below in Part 2.2 for this methodology. 

Once this is complete, we will feed this result into `src/aggregation_validator.py`. This provides us the final confidence values necessary to train our models. 

This concludes the completed work. 

### Work Remaining (8 pts)

The following still remains, but is unfortunately contingent upon having the data of the HITs:

- Analytics of MTurk Results (3pts): This is indeed actually somewhat completed above in the aggregation module. We simply need to extend it to analyzing between posts and also ingesting the information from the original corpus to compare with the turkers. 
- ML Predictor: We plan to use an NLP predictor. However, since ML is often as much as an art as it is science, we have refrained from beginning this phase until we understand our dataset more. Due to the size of the model, we envision the need of multiple techniques for this to work. Further, due to the imbalance of posts found in our dataset, we believe some data manipulation may be needed such as oversampling or imputation. 



## Part 2.2: QC and Aggregation

### Raw Data Input

We take in the data from prior Reddit posts. In particular, we use a Kaggle dataset that used PRAW in 2020 to scrape the r/AmITheAsshole subreddit. Luckily, the r/AmITheAsshole contains a bot (the only bot that is allowed for the subreddit, since it has strict rules), that will classify the post given the four criteria (YTA, NTA, ESH, and NAH) as a tag for the post given the comments for the given post. WE use this data as the input for our criteria analysis, and the baseline for our comparison between crowdworkers and redditors. See: https://www.kaggle.com/spectrumpositive/praw-scrapings-from-ramitheasshole

Example Raw Data is found at: `/data/raw0207.csv`

### Aggregation Module
The aggregation module is comprised of HIT 1's questions which is the result from HIT 1. Once HIT 1 is complete, the questions must be aggregated together to develop the batch CSV for HIT 2. 

## HIT 1 to HIT2 Aggregation

Big Idea: At a high level, this component takes id, AITA title, AITA body, three questions, one correct answer choice for each question, and two incorrect answer choices for each question. Then grouping each answer set (the three answer choices associated with each question), it stores them in a list. Then, the choices are randomly sorted through a randomizer. This is done so that the correct answer choice is not always in the same position everytime. This would defeat the putpose of the quality control. After randomization, it displays the output. 

_Sample Input:_ `/data/agg_hit1_input.csv` [Provides raw input from HIT1]

_Sample Output:_ `/data/agg_hit1_output.csv`[Aggregate the HIT1 to create the input for HIT2]
                `/data/agg_key.csv`[Aggregate the key to the comprehension questions]

_Code:_ `/src/aggregation_validator.py`


## Post HIT 2 Aggregation

In HIT 2 or what we are calling the validation HIT, we get user answers on the 3 comprehension questions, and thier opinion on whether the author behaved in an insensitive way or not. We first use the answers on the comprehension questions as gold standard questions to verify whether the user has actually read through the body of the text. We then weight the label of the user by their accuracy on the three questions. Then we aggregate all the answers for a particular prompt into one label by choosing the label with the highest weighted score, and get the confidence of that label by dividing the weighted score of that label by the sum of the weighted scores of all the labels.

Once we have cleaned and wrangled the kaggle dataset we will expand the functionality of this file by getting the labels the reddit audience also used, and then we will use the two different sets of labels for more analysis.

_Sample Input:_ `data/agg_hit_2_input.csv` [Has raw user answers for comprehension and validator after HIT2]

_Sample Output:_ `data/agg_hit_2_output.csv` [Final labels after aggregating data w/ confidence levels]

_Code:_ `src/aggregation_validator.py`

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
