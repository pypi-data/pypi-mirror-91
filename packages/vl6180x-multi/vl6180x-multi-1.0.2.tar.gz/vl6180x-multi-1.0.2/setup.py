import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vl6180x-multi",
    version="1.0.2",
    author="Vitaly Grinberg",
    author_email="vtalikgr@gmail.com",
    description="Multiple VL6180X time of flight distance sensors on the same I2C bus.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vitus133/vl6180x_multi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Adafruit-Blinka",
        "adafruit-circuitpython-busdevice",
        "adafruit-circuitpython-lis3dh",
        "adafruit-circuitpython-vl6180x",
        "Adafruit-PlatformDetect",
        "Adafruit-PureIO",
        "pigpio",
        "pkg-resources",
        "pyftdi",
        "pyusb",
        "rpi-ws281x",
        "RPi.GPIO",
        "sysv-ipc"
    ],
)