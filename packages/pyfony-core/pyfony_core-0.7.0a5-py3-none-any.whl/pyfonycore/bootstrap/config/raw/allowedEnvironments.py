def get(rawConfig):
    return rawConfig['allowedEnvironments'] if 'allowedEnvironments' in rawConfig else ['dev', 'test', 'prod']
