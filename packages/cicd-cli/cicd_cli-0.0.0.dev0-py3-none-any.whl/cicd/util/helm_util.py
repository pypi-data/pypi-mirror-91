import subprocess
from cicd.util import aws_util

def deploy(application_name, lifecycle, version, chart):
    repository = aws_util.get_repository(application_name, lifecycle)
    repository_uri = repository['repositoryUri']
    opts = [
        '--install',
        '-f', '.cicd_config.yml',
        '-n', lifecycle,
        '--set', f"deployment.image={repository_uri}",
        '--set', f"deployment.version={version}",
        '--set', f"deployment.env.LIFECYCLE={lifecycle}",
        application_name, chart,
    ]
    helm('upgrade', opts)

def delete(application_name, lifecycle):
    helm('delete', [
        '-n', lifecycle,
        application_name,
    ])

def update_repo():
    helm('repo', ['add', 'pago', 's3://pago-charts'])
    helm('repo', ['update'])

def helm(action, opts=[]):
    command = ['helm', action]
    command.extend(opts)
    subprocess.run(command, check=True)
