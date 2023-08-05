import subprocess

def run_tests(capture_output=False):
    return python('setup.py test')

def build():
    return python('setup.py sdist bdist_wheel')

def get_version():
    version_output = python('setup.py --version', capture_output=True).stdout
    return version_output.decode("utf-8").strip()

#def publish(lifecycle='dev': str):
#    if lifecycle
    
def python(args: str, path='python3', capture_output=False):
    command = [ path ]
    args = args.split(' ')
    command.extend(args)
    return subprocess.run(
        command,
        check=True,
        capture_output=capture_output,
    )
