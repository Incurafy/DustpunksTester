# utils.py

def clamp(value, min, max):
    return min if value < min else max if value > max else value