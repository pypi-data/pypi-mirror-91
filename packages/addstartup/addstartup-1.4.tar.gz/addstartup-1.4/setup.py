from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='addstartup',
      version='1.4',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='a package for Add File to Windows Startup',
      url='https://www.youtube.com/channel/UCGsKXfbCyhZoLIRukYUQyYQ',
      author='MD Trackers',
      author_email='mdtrackersother@gmail.com',
      license='MDTrack',
      packages=['addstartup'],
      zip_safe=False)