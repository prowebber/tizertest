import os

# correct path from pycharm bullshit
[os.rename(f, f.replace('\\', '/')) for f in os.listdir()]
