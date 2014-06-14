import os

def makedir_if_absent(directory_name):
    try:
        os.makedirs(directory_name)
    except OSError:
        if os.path.exists(directory_name):
            pass
        else:
            raise
