import yaml
import os

def test_render_yaml_structure():
    render_yaml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'render.yaml')
    with open(render_yaml_path, 'r') as f:
        render_config = yaml.safe_load(f)

    assert 'services' in render_config
    assert 'databases' in render_config
    assert 'secretFiles' in render_config

    services = {service['name']: service for service in render_config['services']}
    assert 'frontend' in services
    assert 'backend-api' in services
    assert 'data-poller' in services
    assert 'trading-engine' in services
    assert 'redis' in services

    databases = {db['name']: db for db in render_config['databases']}
    assert 'user-db' in databases
    assert 'general-db' in databases

    secret_files = {sf['name']: sf for sf in render_config['secretFiles']}
    assert 'master-key' in secret_files

    backend_api = services['backend-api']
    env_vars = {env['key']: env for env in backend_api['envVars']}
    assert 'DATABASE_URL_USER' in env_vars
    assert env_vars['DATABASE_URL_USER']['fromDatabase']['name'] == 'user-db'
    assert 'DATABASE_URL_GENERAL' in env_vars
    assert env_vars['DATABASE_URL_GENERAL']['fromDatabase']['name'] == 'general-db'
    assert 'REDIS_URL' in env_vars
    assert env_vars['REDIS_URL']['fromService']['name'] == 'redis'

    assert 'secretFiles' in backend_api
    backend_secrets = {sf['name']: sf for sf in backend_api['secretFiles']}
    assert 'master-key' in backend_secrets 