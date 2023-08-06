import setuptools

setuptools.setup(
    name="doubleagent",
    version="1.12",
    license='MIT',
    author="complexplayer",
    author_email="didutc@gmail.com",
    description="Double list makes a list",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
