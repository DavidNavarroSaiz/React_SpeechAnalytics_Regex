## Azure React Regex

This demo is an extension of the [Speech-Recognition-React](https://github.com/DavidNavarroSaiz/Speech-Recognition-React) project, it is a webdemo implemented in React, but the main difference is that the analytics of the speech is not done using NER but in this case it is used Regular expressions, this was done in python, as an API using FastAPI and the web application comsumes sad API. because it is rule-based a lot of data can be extracted but it is necesary to check all the cases of the speech of a person, and it has to be done in two languages(spanish, english) and processing times for this API was close to the 20 seconds,which is not appropiate for this solution.

## How to run 

### Regex_API:
go to the 'Azure_React_regex/regex_api'

Create a new environment
```
    python3.8 -m venv <env_name>
```
if you are using anaconda you just can write the following code line:

```
    conda create --name <env_name> python=3.8
```
activate the envitonrment:

```
    cd <env_name> \Scripts\activate.bat
```

<p>Anaconda:<p>

```
    conda activate <env_name>
```
```    
    conda install pip
    pip install -r requirements.txt
```

run in the terminal:
```
uvicorn main:app --reload

```
ht eapp now is running at:

`http://127.0.0.1:8000`

to learn what are the endponts and how to interact with the app open the following link at the explorer:

`http://127.0.0.1:8000/docs`


### Speech Recognition APP

- you have to install the packages so in the speech_recognitio_app folder runthe comman:
`npm install` 

then create a .env file and copy paste the following variables:

```
REACT_APP_SUBSCRIPTION_KEY=""
REACT_APP_SERVICE_REGION=""

```


in each variable set the corresponding key:

REACT_APP_SUBSCRIPTION_KEY and REACT_APP_SERVICE_REGION are related with the speech recognition and the speech to text modules of azure.[azure portal](https://portal.azure.com/)




## What you will find:

in the `./scr/app.js` file you will find 5 important functions:

### startRecognition():

is the function that get access to the microphone and start the speech recognition, this function is divided in 4 events that are related with the recognizer engine.

speechRecognizer.recognizing : displays in realtime what is the engine recognizing from the speech

speechRecognizer.recognized: when the user makes a pause in the speechit will take that pause as the beggining of a new phrase, so it will start again a new phrase and will separate the phrases by period(. ) at the moment that the user makes a pause the recognized event will be triggered

speechRecognizer.canceled: if the speech recognition fails or is it canceled then this event is activated.

speechRecognizer.sessionStopped: if it is used the command speechRecognizer.stopContinuousRecognitionAsync then the event will be triggered.


startRecognition functiontriggers the speech recognition module with the following command:
speechRecognizer.startContinuousRecognitionAsync()

### stopRecognition():

it is a function that activates the function speechRecognizer.stopContinuousRecognitionAsync();
which stops the recognition.

### clearResult():

the function cleans all the text areas in the web app, and the main variables, that is done to start again from the beggining

### Analyze results():

It makes a request to the API `http://127.0.0.1:8000/extract_info` the API returns a json with the following structure:
```
response = {
        "Name": name,
        "Age": age,
        "Location": location,
        "Address": address,
        "date": dates,
        "phone": phone,
        "Email": emails,
        "Areas_of_Interest": areas_of_interest,
        "Goals": goals
    }
then the response is verified and the values are set in the corresponding text areas
    ```

### textToSpeech():

this is a function that uses Azure SpeechSDK to perform text to speech, it takes the text in the `text_to_speech` cell, and reades with a default voice of azure, that voice can be changed deppending on the language. works on different languages.

