from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'PlotMyGoogleSheet28',
    version = '0.0.1',
    description = 'This package will help you to plot a chart betweem any two columns from google sheet',
    long_description = long_description + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type = 'text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10'],
    keywords = 'Graph Google-Sheet',
    url = '',
    author = 'Aditya Sisodiya',
    author_email = 'adityasisodiya2803@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['gspread==3.6.0', 'matplotlib==3.1.1', 'pandas==1.1.0', 'seaborn==0.11.1', 'gspread-dataframe==3.2.0'],
    include_package_data = True,
    zip_safe = False
)