# Experiment 8: ML utility with DELIBERATE vulnerabilities (to scan)
import pickle
import subprocess
import hashlib

def load_model(path):
    # VULNERABLE (B301): pickle.load on untrusted data -> code execution
    with open(path, "rb") as f:
        return pickle.load(f)

def run_cmd(user_input):
    # VULNERABLE (B602): shell=True with user input -> command injection
    return subprocess.call(user_input, shell=True)

def checksum(data):
    # VULNERABLE (B324): MD5 is cryptographically broken
    return hashlib.md5(data.encode()).hexdigest()

# VULNERABLE (B105): hard-coded secret
DB_PASSWORD = "admin123"