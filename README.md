Simple browser game

### Setup
First, clone the repository:

```sh
$ git clone https://github.com/aperushin/arena-game
$ cd arena-game
```

Create and activate virtual environment:
```sh
$ python -m venv venv
$ source venv/bin/activate
```

Install project requirements:
```sh
(venv)$ pip install -r requirements.txt
```


### How to run

```sh
(venv)$ python -m flask run -h 127.0.0.1 -p 5000
```

The game should be available on http://127.0.0.1:5000
