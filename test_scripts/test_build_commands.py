"""Check CMake command construction without invoking the native toolchain."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from setuptools import Distribution

from extensions import NLOptBuild, NLOptBuildExtension


class BuildCommandsTest(unittest.TestCase):
    def test_generator_neutral_parallelism_and_build_type(self):
        for system in ('Windows', 'Linux'):
            for debug in (False, True):
                with self.subTest(system=system, debug=debug), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    command = NLOptBuild(Distribution({'version': '2.11.0'}))
                    command.build_temp = str(root / 'temp')
                    command.build_lib = str(root / 'lib')
                    command.debug = debug
                    extension = NLOptBuildExtension('nlopt._nlopt', '2.11.0')
                    extension_path = root / 'lib' / 'nlopt' / '_nlopt.pyd'
                    extension_path.parent.mkdir(parents=True)
                    calls = []

                    def execute(cmd, cwd, calls=calls, **kwargs):
                        calls.append(cmd)
                        if '--build' in cmd:
                            wrapper = cwd / 'extern/nlopt/src/swig/python/nlopt.py'
                            wrapper.parent.mkdir(parents=True)
                            wrapper.write_text('# generated test fixture\n')

                    with patch('extensions.platform.system', return_value=system), \
                         patch.object(command, 'get_ext_fullpath', return_value=str(extension_path)), \
                         patch('extensions.execute_command', side_effect=execute), \
                         patch.dict(os.environ, {'CMAKE_BUILD_PARALLEL_LEVEL': '2'}):
                        command.build_extension(extension)
                    config = 'Debug' if debug else 'Release'
                    self.assertIn(f'-DCMAKE_BUILD_TYPE={config}', calls[0])
                    self.assertEqual(calls[1], ['cmake', '--build', '.', '--config', config, '--parallel', '2'])


if __name__ == '__main__':
    unittest.main()
