# coding:utf-8
# author: zhao heng ping

try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="excel_picture",
    packages=find_packages(),
    version='0.0.1',
    description='This is a tool that can quickly locate the path of the picture, it is very easy to use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xizhicode/excel_picture.git',
    author='zhaohengping',
    author_email='13073771301@163.com',
    maintainer='zhaohengping',
    maintainer_email='zhaohengping@gongchang.com',
    install_requires=["shutil", "xlrd", "zipfile"],
    include_package_data=True,
    entry_points={
                  'console_scripts': [
                      'excel_picture=excel_picture.__init__:main',
                  ],
              },
    package_data={
            '': ['*.rst'],
        },
    python_requires='>=3.6',
    license='GPL-2.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
