import setuptools

setuptools.setup(
    name='aiohttp_but_its_requests',
    version='0.1.0',
    author='TriC',
    description='The speed of aiohttp simplified to the level of requests.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.6',
    keywords=['aiohttp','requests','fast'], 
    include_package_data=True,
    install_requires=['aiohttp', 'nest_asyncio']
)
