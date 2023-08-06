from setuptools import setup
import sushi

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sushi-sub',
    description='Automatic subtitle shifter based on audio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['sushi'],
    version=sushi.VERSION,
    url='https://github.com/FichteFoll/Sushi',
    project_urls={
        'Documentation': 'https://github.com/tp7/Sushi/wiki',
        'Fork Origin': 'https://github.com/tp7/Sushi',
    },
    license='MIT',
    python_requires='>=3.5',
    install_requires=['numpy>=1.8'],
    entry_points={
        'console_scripts': [
            "sushi=sushi.__main__:main",
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Text Processing',
    ]
)
