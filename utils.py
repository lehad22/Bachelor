import numpy as np
import base64
import netCDF4 as nc

def calculate_statistics(data):
    mean_value = np.mean(data)
    median_value = np.median(data)
    std_deviation = np.std(data)
    return mean_value, median_value, std_deviation

def save_uploaded_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with open(filename, 'wb') as f:
        f.write(decoded)
