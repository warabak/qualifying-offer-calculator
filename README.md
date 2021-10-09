# The Qualifying Offer Calculator

## Description

This is an application for calculating a qualifying offer for MLB based on a population of player salary data.

It contains two run modes :

1. A simple command line interface :

```
python runner.py --help
Usage: runner.py [OPTIONS]

Options:
  --number_of_salaries INTEGER  The number of highest salaries to use when
                                calculating the qualifying offer
  --show_top_salaries           Optionally show the top players salaries
  --verbose                     Run the program in verbose mode
  --help                        Show this message and exit.
```

2. A simple Flask app that renders a website

![calculator-screen-shot.png](docs/images/calculator-screen-shot.png)

## CLI Demo

![cli-demo](docs/images/cli-demo.gif)

## Website Demo

![website-demo](docs/images/website-demo.gif)

## Setup

1. Create and activate a virtual environment with python 3.8+
    1. This project uses python version 3.8.12 specifically and has been configured using pyenv & pyenv-virtualenv
2. Install the requirements :
    1. `pip install -r requirements.txt`
3. Try out the command line interface first :
    1. `python runner.py --verbose`
4. Finally, try out the flask app :
    1. Run `python app.py`
    2. Go to http://localhost:5000/calculator
    3. Play around with the data! You can search, sort, and adjust the number of players used in calculating the
       qualifying offer with the query parameter number_of_salaries=99