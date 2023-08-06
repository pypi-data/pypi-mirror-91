from typing import List
from injecta.dtype.classLoader import loadClass
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import entryPointsReader, pyprojectReader

def getEntryPoints():
    entryPoints = entryPointsReader.getByKey('pyfony.bundle')

    for entryPoint in entryPoints:
        _checkName(entryPoint.name, entryPoint.value)

    return entryPoints

def loadBundles() -> List[Bundle]:
    bundles = [entryPoint.load()() for entryPoint in getEntryPoints()]

    rawConfig = pyprojectReader.read(pyprojectReader.getPath())

    if _entryPointDefined(rawConfig):
        bundle = _loadDirectly(rawConfig)()
        bundles.append(bundle)

    return bundles

def _entryPointDefined(rawConfig):
    return (
        'tool' in rawConfig
        and 'poetry' in rawConfig['tool']
        and 'plugins' in rawConfig['tool']['poetry']
        and 'pyfony.bundle' in rawConfig['tool']['poetry']['plugins']
    )

def _loadDirectly(rawConfig):
    entryPoints = rawConfig['tool']['poetry']['plugins']['pyfony.bundle']

    for name, val in entryPoints.items():
        _checkName(name, val)

    return _parse(entryPoints['autodetect'])

def _checkName(name: str, value):
    if name != 'autodetect':
        raise Exception(f'Unexpected entry point name "{name}" for {value}')

def _parse(val):
    moduleName, classAndMethod = val.split(':')
    className, functionName = classAndMethod.split('.')

    class_ = loadClass(moduleName, className) # pylint: disable = invalid-name

    return getattr(class_, functionName)
