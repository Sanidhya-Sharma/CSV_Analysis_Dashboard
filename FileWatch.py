import pandas as pd
import numpy as np
import os
import time
        
def watch_file(filename, time_limit=5, check_interval=1):

    now = time.time()
    last_time = now + time_limit

    while time.time() <= last_time:
    
        if os.path.exists(filename):
            return True
        
        else:
            time.sleep(check_interval)
            print("Checking...")
    return False

