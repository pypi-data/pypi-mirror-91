

from setuptools import setup

long_description='''This module has four submodules :siteinfo, sitemapping,  sitelocation, and aircom.
Each of these submodules have different uses. Siteinfo can be used to find the sites: encoding, cookies, ip and port, and
header.   Sitemapping is used to: check if a url is valid and online,  map all internal and external urls on a site,
and find all hidden urls on a site like robot.txt.  Sitelocation is still in development but in the future it will be used
mainly for pulling up a heatmap of the world based on traffic, where the sites server is located and more. aircom is used
for tracking the traffic on a website. To use aircom you will have to have a google API key and include that key in the attributes of the functions.

'''
setup(
   name='pyClockTower',
   version='1.0.0',
   description='A module that allows the user to check the status and attributes of a website',
   license="MIT",
   long_description=long_description,
   author='Seaver Olson',
   author_email='Sjolson007@gmail.com',
   packages=['pyClockTower'], 
)
