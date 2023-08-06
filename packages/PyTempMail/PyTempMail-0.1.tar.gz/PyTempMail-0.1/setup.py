from setuptools import setup, find_packages
setup(name="PyTempMail", version="0.1", author="Shivanshu Mishra", description="Unoffical Python binding for TempMail website", url="https://github.com/Shivanshu10/PyTempMail", packages=find_packages(), classifiers=["Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
], python_requires='>=3.6', install_requires=["selenium"])