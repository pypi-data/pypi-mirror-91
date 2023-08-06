import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aminos", # Replace with your own username
    version="1.0.0.0",
    author="kira_xc",
    author_email="noemail@example.com",
    description="login sid in amino with Amino.py ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kira-xc",
    keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'kira_xc'
        
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'websocket-client',
        'Amino.py'
    ],
    setup_requires = [
        'wheel'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)