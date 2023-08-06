from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from pyfonybundles.loader import pyfonyBundlesLoader
from pyfonycore.bootstrap.config.Config import Config

def initContainer(appEnv: str, bootstrapConfig: Config) -> ContainerInterface:
    bundles = pyfonyBundlesLoader.loadBundles()

    kernel = bootstrapConfig.kernelClass(
        appEnv,
        resolvePath(bootstrapConfig.rootModuleName) + '/_config',
        YamlConfigReader(),
        bundles,
    )
    kernel.setAllowedEnvironments(bootstrapConfig.allowedEnvironments)

    return kernel.initContainer()
