import setuptools

setuptools.setup(name="tkcalc",
                author="Elia S. Toselli",
                author_email="elia.toselli@outlook.it",
                url="https://test.pypi.org/project/tkcalc",
                version="1.3.11",
                packages=['tkcalc'],
                requires="tkinter",
                description="Calcolatrice di base con tkinter",
                entry_points = {
                    'console_scripts': ['tkcalc=tkcalc.app:main'],
                }
)
