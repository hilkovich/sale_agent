import subprocess

def install(name):
    subprocess.run(["pip", "install", "-r", name])
    
install("requirements.txt")
