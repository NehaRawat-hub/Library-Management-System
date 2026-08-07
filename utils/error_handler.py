from utils.logger import error

def handle_exception(username, module, operation, exc):
    error(username, module, operation, exc, "HIGH")
