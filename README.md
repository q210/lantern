## About
Test TCP lantern client for ivideon.

By default this program will show UI drawn with tkinter but there is
console representation too.
Logging, network, UI settigns can be changed in `src/lantern/config.py`

## Install requirements:
    pip install -r requirements.txt

## Install app
    python setup.py install

## Usage
    lantern-app [options]

    Options:
      -h, --help            show this help message and exit
      -c COLOR, --color=COLOR
                            initial lantern color
      -p, --powered         initial lantern power state
      --console             use console lantern

### Run tests:
    py.test

### Start mock server:
    python src/mock_server.py

### Try from console without installing:
    python src/lantern/app.py --console
