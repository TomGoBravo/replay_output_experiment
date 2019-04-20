from setuptools import setup, find_packages

requires = [
    "avro-python3",
    "colorlog==3.1.4",
    "fastavro",
    "faust==1.5.4",
    "robinhood-aiokafka==1.0.2",
    "requests",
    "simple-settings==0.16.0",
]

setup(
    name="Replay Output Experiment",
    version="0.1.0",
    description="Experiment using faust to replay the output topic",
    long_description="""Experiment using faust to replay the output topic""",
    classifiers=["Programming Language :: Python"],
    author="Tom Brown",
    author_email="tomgith4@thecap.org",
    url="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "replay_output_experiment = replay_output_experiment.app:main"
        ]
    },
)
