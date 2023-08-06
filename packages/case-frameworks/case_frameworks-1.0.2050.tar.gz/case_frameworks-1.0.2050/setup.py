from setuptools import setup
'Note: To upload new versions 1) cd to GOCPI 2) python setup.py sdist 3) twine upload dist/*'
'Note: To download 1) pip install --upgrade case_frameworks'
'Note: Make your own python package: https://towardsdatascience.com/make-your-own-python-package-6d08a400fc2d'
'Note: PyPi https://pypi.org/manage/project/gocpi-functions/releases/#modal-close'
'Note: Enter dist/GOCPI-X.X.X.tar.gz to upload one file'

setup(name='case_frameworks',
      version='1.0.205',
      description='Functions and Class for Consulting Preparation',
      packages=['case_frameworks'],
      author_email='connormcdowall@gmail.com',
      zip_safe=False)

'/Users/connor/Google Drive/Documents/Professional/Projects/Consulting/case_frameworks'