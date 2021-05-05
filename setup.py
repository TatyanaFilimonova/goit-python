from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='Clean folder script',
    url='https://github.com/TatyanaFilimonova/goit-python',
    author='Tatyana Filumonova',
    author_email='tatyana0377@gmail.com',
    license='MIT',
    packages=find_namespace_packages()
    install_requires=['markdown'],
    entry_points={'console_scripts': ['clean-folder.clean:main']}
)
