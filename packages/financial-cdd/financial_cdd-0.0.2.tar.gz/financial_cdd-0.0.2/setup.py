import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="financial_cdd", 
    version="0.0.2",
    author="Filippo Neri",
    author_email="filippo.neri.email@gmail.com",
    description="Concept drift detectors for financial time series",
    long_description="Concept drift detectors for financial time series. It is appreciated the citation of the author and the study. Filippo Neri (2021). Domain Specific Concept Drift Detectors for Predicting Financial Time Series, Preprint. Available at: https://www.researchgate.net/publication/348371870_Domain_Specific_Concept_Drift_Detectors_for_Predicting_Financial_Time_Series ",
    long_description_content_type="text/markdown",
    url="https://github.com/filipponeri/financial_cdd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
