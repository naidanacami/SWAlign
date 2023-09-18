# SWAlign
 This program aligns elements on two documents. This program was made specifically made for SolidWorks but may function in other applications.

# Installation
## Stable install
1. Install SWAlign.exe from the [latest release](https://github.com/naidanacami/SWAlign/releases)
2. run SWAlign.exe

## Dev install (unstable)
1. Download code
    ```
    git clone https://github.com/naidanacami/SWAlign.git
    ```
2. Unzip
3. Install requirements
    ```
    pip install -r requirements.txt
    ```
- run SWAlign.py
    ```
    python SWAlign.py
    ```


# Instructions:
[Video instructions](https://youtu.be/I8ebZESkd9c)

1. Define top left and bottom right bounds of both the origianl and the working document.
   - DO NOT move the document after defining its corners (otherwise the program will fail)
2. Define a common point on an object on each document.
3. Let go of HID until SWAlign moves the object
    - To move SolidWorks dimensions, hold alt while the program moves the element
