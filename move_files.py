import os

# correct path from pycharm bullshit
[os.rename(f, f.replace('\\', '/')) for f in os.listdir()]

# Correct tabs (\\t) in file name bullshit
[os.rename(f, f.replace('\t', '/t')) for f in os.listdir()]

# Correct (\\r) in file name bullshit
[os.rename(f, f.replace('\r', '/r')) for f in os.listdir()]