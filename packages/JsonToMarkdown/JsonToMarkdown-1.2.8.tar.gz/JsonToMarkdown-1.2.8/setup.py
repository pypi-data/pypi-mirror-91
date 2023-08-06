"""
Documentation
-------------
nothing

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="JsonToMarkdown",
        description="Convert Json to Markdown",
        keywords="json markdown",
        long_description=long_description,
        version="1.2.8",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=find_packages(),
        #packages=["JsonToMarkdown"],
        package_data={},
        entry_points={
            'console_scripts':[
                'jsontomd=JsonToMarkdown.main:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
