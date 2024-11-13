# Autovideo

### This repository is for Chulalongkorn University COM PROG (2190101) Course.

## Description
An video generator using OpenAI's whisper to transcribe audio and getting image from pexel and using ffmpeg to put everything together.

## Quickstart

### Prerequisite
Must have ffmpeg and python installed.

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
* <mark>--model</mark>  Select which whisper AI model to use (defaulted at "medium.en")
* <mark>--apikey</mark> Attach api key for pexel use if not in enviroment variable
