@echo off
set comPort=%~1
set binaryPath=%~2
1-10_MP_Image_Tool.exe -set chip amebad

::: First Binary Start :::
set "binaryFile=%binaryPath%\km0_boot_all.bin"
set "binarySize=0"
call:toHex %binaryFile%
1-10_MP_Image_Tool.exe -set image "%binaryFile%"
1-10_MP_Image_Tool.exe -set address 0x08000000
1-10_MP_Image_Tool.exe -set length 0x%binarySize%
1-10_MP_Image_Tool.exe -download %comPort%
::: First Binary End :::

::: Second Binary Start :::
set "binaryFile=%binaryPath%/km4_boot_all.bin"
set binarySize=%binaryFile%
call:toHex %binarySize%
1-10_MP_Image_Tool.exe -set image "%binaryFile%"
1-10_MP_Image_Tool.exe -set address 0x08004000
1-10_MP_Image_Tool.exe -set length 0x%binarySize%
1-10_MP_Image_Tool.exe -download %comPort%
::: Second Binary End :::

::: Third Binary Start :::
set "binaryFile=%binaryPath%/km0_km4_image2.bin"
set binarySize=%binaryFile%
call:toHex %binarySize%
1-10_MP_Image_Tool.exe -set image "%binaryFile%"
1-10_MP_Image_Tool.exe -set address 0x08006000
1-10_MP_Image_Tool.exe -set length 0x%binarySize%
1-10_MP_Image_Tool.exe -download %comPort%
::: Third Binary End :::

::: Fouth Binary Start :::
set "binaryFile=%binaryPath%/fs.bin"
set binarySize=%binaryFile%
call:toHex %binarySize%
1-10_MP_Image_Tool.exe -set image "%binaryFile%"
1-10_MP_Image_Tool.exe -set address 0x08380000
1-10_MP_Image_Tool.exe -set length 0x13880
1-10_MP_Image_Tool.exe -download %comPort%
::: Fouth Binary End :::

EXIT /B 0

:toHex
SETLOCAL ENABLEDELAYEDEXPANSION
set "binaryFileName=%~1"
FOR /F "usebackq" %%A IN ('%binaryFileName%') DO set size=%%~zA
set /a dec=size
set "hex="
set "map=0123456789ABCDEF"
for /L %%N in (1,1,8) do (
    set /a "d=dec&15,dec>>=4"
    for %%D in (!d!) do set "hex=!map:~%%D,1!!hex!"
)
for /f "tokens=* delims=0" %%A in ("%hex%") do set "hex=%%A"&if not defined hex set "hex=0"
echo %binaryFileName%
echo %size%
echo %hex%
( ENDLOCAL
    set "binarySize=%hex%"
)
EXIT /B 0
