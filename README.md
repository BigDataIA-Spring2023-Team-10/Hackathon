# Hackathon

# MediBot
"Empowering Patients, One Symptom at a Time."

[![PyPI](https://img.shields.io/pypi/pyversions/locust.svg)](https://pypi.org/project/locust/)



![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)


# Codelabs Documentation

>[Access the Codelabs document here](https://codelabs-preview.appspot.com/?file_id=1OMODb5qxvAS9P0_J97sy1icvkCxuiHOrHvm_0oLl6yI#2) 🚀 <br>
> [🚀 Application link](https://bigdataia-spring2023-team-10-hackathon-home-kh1paw.streamlit.app/)<br>






# Overview 📝

We have built a meeting intelligence application that reads an audio file, converts the audio into transcript using Whisper Api and then using GPT 3.5 Api, runs queries and asks questions related to the meeting. For frontend we have used Streamlit and scheduled tasks of reading audio, creating transcript and running default queries using Apache-Airflow.


# Process Outline

>1. We are creating 2 DAGs, first Adhoc (runs on single audio file), second Batch (runs on a batch of audio files)

>2. Download audio file from GCP.

>3. Read and convert audio to transcript using Whisper Api

>4. Pass the transcript along with related queries through GPT 3.5 API.

>5. Store user activity logs(Queries) into DB.





# Project Stcuture 











## How to use  this project:


1. Clone this repo locally `git clone <repo-url>`

2. Setup the local python enviornment.

3. Install all the dependencies from the requirements.txt file
`pip install -r requirements.txt`

4. Install all local dependencies 
`pip install -e .`

5. Create `.env` file.













### Team Member

| NUID | Team Member       |
|:-----:|---------------|
| 002766036       | Anuj Kumar |
| 002794258      |  Hitesh  Pant            |
| 002773080      |  Kunal Bhoyar              |
| 002772221      |  Snehashis Lenka              |


WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.







