from setuptools import setup, find_packages

setup(
    name="noip_updater",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "noip-updater=noip_updater.cli:main",
        ],
    },
    description="Автоматичний постійно активний модуль для оновлення IP на No-IP",
    author="Дмитро Колоднянський",
    author_email="gosdepyxa@google.com",
    url="https://github.com/DepyXa/upd_noip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
