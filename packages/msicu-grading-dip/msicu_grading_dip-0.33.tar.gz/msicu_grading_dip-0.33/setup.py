import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='msicu_grading_dip',  
     version='0.33',
     author="Arturo Curiel",
     author_email="me@arturocuriel.com",
     description="Grading for MSICU DIP class (Mexico)",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/MSICUDIP",
     packages=setuptools.find_packages(),
     install_requires=['numpy', 'unidecode', 'sklearn'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     package_data={
         "msicu_grading_dip": ["resources/*"],
     },
     entry_points = {
        'console_scripts': ['check_one=msicu_grading_dip.one:main',
                            'check_two=msicu_grading_dip.two:main',
                            'check_project=msicu_grading_dip.project:main'],
     },
 )
