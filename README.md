# ML-service - comment sentiment analysis with BERT, Pytorch, Flask and Docker 

## Introduction

This is an ML service to return sentiment based on the content of the comment. Project consists of wrapper based on Transformers (for managing BERT model) and Pytorch that achieves 93% accuracy on quessing positivity / negativity on IMDB reviews. Flask was used to prepare simple web application where user can give provide any comment as an input and get result for sentiment analysis. Docker was used to containerize the application

##  IMDB dataset
IMDB dataset having 50k movie reviews for natural language processing was used to fine-tune BERT and train our model. This is a dataset for binary sentiment classification containing 25,000 highly polar movie reviews for training and 25,000 for testing. For more details regarding the data, go through the following link, 

https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

## Fine-tuning BERT for an IMDB reviews dataset using Pytorch
BERT base model (uncased) is a pretrained model on english language using a masked language modelling objective. As this model is uncased, it does not make a difference between english and English. For more details on the model visit the link given below:

https://huggingface.co/bert-base-uncased

Eventhough I aimed for training the model on 10 epochs, as it was taking too long (~1.5hr for 1 epoch) and as it gave 93% accuracy just after 1 epoch, I finished training my model just on one epoch. Accurary was chosen as a metric for the task as the model itselt is binary classification with balanced distribution of each class.

This repo includes all required python files to train the model on your local machine. In case of trying to train model on local machine, you can change device setting to "cuda" and change torch version that accepts gpu training. (change torch version in requirements.txt for gpu training is required). The model that I am using is trained on google colab and downloaded to be used in the project. Model training jupyter notebook is also included in the repo. (final_bert_sentiment.ipynb)

Note that for running the application you don't need to train the model, as already trained model is included in the project.

## Web Application

The model itself is trained based on binary snetiment which gives positive or negative sentiment. The application is consist of two parts:

**/ (main page)**

On main page  you can provide any comment as an input and get sentiment result as an output. Even though the model was originally trained on binary sentiment, I divided results to positive, neutral and negative sentiments based on probability of of positivity. Please see the ./docker_workspace/app.py for the details. 

<p align='center'>
  <a href="#"><img src='https://raw.githubusercontent.com/Vusal123/sentiment_analysis/main/images/main_page.png' width="700" height="600"></a>
</p>

**/predict (prediction retrieval page)**

On supplementary prediction retrieval you can directly input you comment as http://localhost:5000/predict?sentence=I%20love%20you%20baby which will provide you the result in json format with the probabilities for positive and negative sentiments.

<p align='center'>
  <a href="#"><img src='https://raw.githubusercontent.com/Vusal123/sentiment_analysis/main/images/predict_page.png' width="700" height="600"></a>
</p>

## Installation

Start installation with downloading the repo to your local machine.

NOTE: ```<ABSOLUTEPATH>``` in all commands given below means direct path to file/folder

### Docker build
```
cd <ABSOLUTEPATH>/docker_workspace
docker build -f Dockerfile -t lsml_final_project .
```

Above docker build command will build Docker image from a Dockerfile in the given folder. You can set another name for the image by chaning **"lsml_final_project"** name to any other name.

### Docker run

After Docker will finalize building the image, run:

```
docker run -p 5000:5000 -v <ABSOLUTEPATH>/docker_data/:/root/docker_data/ -v <ABSOLUTEPATH>/docker_workspace/:/root/code/ -ti lsml_final_project /bin/bash -c "cd /root/code/ && python app.py"
```

```<ABSOLUTEPATH>``` for my case was "C:/Users/Vusal/OneDrive/Desktop/final_project_w_docker".

With above given command you application will be ready to run in you local machine. Now, you are good to test the application on any web browser.
