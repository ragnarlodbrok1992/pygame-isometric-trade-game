@echo off
SET compiler="C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.42.34433\bin\Hostx64\x64\cl.exe"

REM relative to build directory
SET sdl_dir=..\c_isometric_engine\ext\sdl\
SET sdl_build=..\c_isometric_engine\ext\sdl\VisualC\x64\Debug\
SET sdl_include=include
SET sdl_dll=SDL3.dll
SET sdl_lib=SDL3.lib

set DIRECTX_HEADERS_INCLUDE_DIR="..\external\DirectX-Headers\include"

IF NOT EXIST build mkdir build

pushd build

echo Copying dll file...

copy %sdl_build%%sdl_dll% .

echo Compiling...

%compiler% /EHsc /Zi^
  /DEBUG:FULL^
  /INCREMENT:NO^
  /std:c++17^
  /Fe:"isometric_trade_game"^
  ../c_isometric_engine/main.cpp^
  -I%sdl_dir%%sdl_include%^
  /I%DIRECTX_HEADERS_INCLUDE_DIR%^
  user32.lib gdi32.lib d3d12.lib dxgi.lib d3dcompiler.lib^
  /link /LIBPATH:%sdl_build% %sdl_lib%^
  /SUBSYSTEM:CONSOLE /out:IsometricTradeGame.exe

popd

