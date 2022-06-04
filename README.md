# HandRcgInput

Input Application by recognizing hand using OpenCV.

## Process

The process of image processing.

<img src="https://github.com/to-jiki/HandRcgInput/blob/main/img/process1.png" height="50%" width = "50%" >

<img src="https://github.com/to-jiki/HandRcgInput/blob/main/img/process2.png" height="50%" width = "50%" >


## Requirement

This project Using pipenv create Virtual env. Please install pipenv at first.

```bash
$ pip install pipenv
```

Then install requirement from Pipfile

```bash
$ pipenv install
```

## Usage

```bash
python finger.py
```

Window will appear.
Press "B" (keyboard) and captured background , and be careful don't capture things moving in green area.
Then press "j" start to input letter keeping your fingertip in the letter box that you want to input.

### ⚠️

This program is adjust for my circumstance, so it may be doesn't work in general.
