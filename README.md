# Autovideo

## A simple video generator from audio.

## Quickstart

### Prerequisite
Must have ffmpeg installed

### Installation

```
$ virutalenv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

### Setup

Get pexel api key and put it in your enviroment variables or create .env file or put it command line argument


### Usage

```
$python main.py --input <path_to_audio> --output <path_to_output>
```

### Settings
* ==--model==  Select which whisper AI model to use (defaulted at "medium.en")
* ==--apikey== Attach api key for pexel use if not in enviroment variable
