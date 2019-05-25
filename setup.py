from pathlib import Path
from setuptools import setup, find_packages
from typing import List


def parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    requirements = (Path(__file__).parent / filename).read_text().strip().split('\n')
    requirements = [r.strip() for r in requirements]
    requirements = [r for r in sorted(requirements) if r and not r.startswith('#')]
    return requirements


setup(
    name="Replay Output Experiment",
    version="0.1.0",
    description="Experiment using faust to replay the output topic",
    long_description="""Experiment using faust to replay the output topic""",
    classifiers=["Programming Language :: Python"],
    author="Tom Brown",
    author_email="tom-brown@gmail.com",
    url="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements("requirements.txt"),
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "replay_output_experiment = replay_output_experiment.app:main"
        ],
        
        "faust.codecs": [
            "msgpack_codec = replay_output_experiment.codecs.codec:msgpack",
            # add entries here to add more custom codecs
        ],
        
    },
)
