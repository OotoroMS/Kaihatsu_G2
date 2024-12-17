# log_error.py
def log_error(instance, method_name, error):
    print(f"{instance.__class__.__name__}: {method_name}: {error}")