from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.bootstrap.config.raw import containerInitResolver, rootModuleNameResolver, allowedEnvironments

def create(rawConfig, pyprojectSource: str):
    if containerInitResolver.containerInitDefined(rawConfig):
        initContainer = containerInitResolver.resolve(rawConfig, pyprojectSource)
    else:
        from pyfonycore.container.containerInit import initContainer # pylint: disable = import-outside-toplevel

    return Config(
        initContainer,
        rootModuleNameResolver.resolve(rawConfig, pyprojectSource),
        allowedEnvironments.get(rawConfig)
    )
