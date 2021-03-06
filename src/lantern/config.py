# network
HOST = '127.0.0.1'  # or '0:0:0:0:0:0:0:1'
PORT = 9999

# UI
DEFAULT_POWERED = False  # powered off
DEFAULT_COLOR = '#000000'  # black

BACKGROUND_COLOR = '#FFFFFF'  # white
DIMENSIONS = "200x200"
REFRESH_RATE = 100  # UI refresh every 100 milliseconds

# misc
LOGGING = {
    'level': 'INFO',
    'handler': 'StreamHandler',  # or 'FileHandler'
    'filepath': 'lantern.log'
}
