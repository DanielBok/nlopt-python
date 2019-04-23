@rem Sample build script to test build process locally

@rem Start at package directory
set PKG_DIR=%CD%

@rem install numpy, needed to build python
pip install numpy

@rem move up one directory to clone nlopt application
cd ..
git clone https://github.com/stevengj/nlopt

@rem move into build folder
cd nlopt
set APP_DIR=%CD%
mkdir build && cd build

@rem Release configuration
set CONFIG=Release
set CMAKE_PLATFORM=Visual Studio 15 2017 Win64

@rem build package
cmake -G "%CMAKE_PLATFORM%" -DCMAKE_INSTALL_PREFIX="%APP_DIR%\install" ..
cmake --build . --config %CONFIG% --target install

@rem move back to nlopt folder
cd ..

@rem copy dll and python generated files over to package folder
cp install\bin\nlopt.dll %PKG_DIR%\nlopt\nlopt.dll
cp install\lib\site-packages\_nlopt.pyd %PKG_DIR%\nlopt\_nlopt.pyd
cp install\lib\site-packages\nlopt.py %PKG_DIR%\nlopt\nlopt.py
