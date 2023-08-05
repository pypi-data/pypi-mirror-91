import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taskid", # Replace with your own username
    version="0.1.2",
    author="Tiago Botelho",
    author_email="tiagonbotelho@gmail.com",
    description="Taskid client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taskidhq/taskid-python",
    packages=setuptools.find_packages(),
    license="Apache Software License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
