import subprocess

def maven(target, opts='', capture_output=False):
    command = ['mvn']
    if len(opts) > 0:
        command.extend(opts.split(' '))
    if len(target) > 0:
        command.extend(target.split(' '))
    return subprocess.run(command, check=True, capture_output=capture_output)

def install(opts=''):
    maven('clean install', opts)

def get_version():
    versionOutput = maven('exec:exec', "-q -Dexec.executable=echo -Dexec.args='${project.version}' --non-recursive", capture_output=True).stdout
    return versionOutput.decode("utf-8").strip()
