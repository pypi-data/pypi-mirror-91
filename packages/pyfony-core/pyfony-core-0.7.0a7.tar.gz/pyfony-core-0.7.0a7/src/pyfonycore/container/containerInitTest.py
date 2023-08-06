import unittest
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from pyfonycore.Kernel import Kernel
from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.container.containerInit import initContainer

class containerInitTest(unittest.TestCase):

    def test_basic(self):
        config = Config(initContainer, Kernel, 'pyfonycore', ['test'])
        container = config.containerInitFunction('test', config)

        foo = container.get(Foo)
        bar = container.get('injecta.mocks.Bar')

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)

if __name__ == '__main__':
    unittest.main()
