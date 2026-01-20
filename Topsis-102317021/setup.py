from setuptools import setup

setup(
    name="Topsis-Kanishika-102317021",
    version="1.0.0",
    description="TOPSIS command line implementation",
    author="Kanishika",
    author_email="kanishika@example.com",
    py_modules=["topsis"],
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis:topsis"
        ]
    }
)
