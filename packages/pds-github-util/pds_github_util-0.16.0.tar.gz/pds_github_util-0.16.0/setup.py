import re
import setuptools

with open("./pds_github_util/__init__.py") as fi:
    result = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fi.read())
version = result.group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

#with open('requirements.txt', 'r') as f:
#    pip_requirements = f.readlines()
pip_requirements = [ 'github3.py>=1.3',
                     'lxml>=4.5',
                     'mdutils>=1.2',
                     'packaging>=20.4',
                     'markdown2==2.3',
                     'pystache==0.5.4',
                     'emoji==0.5',
                     'gitpython==3.1',
                     'requests==2.23.0',
                     'beautifulsoup4==4.9.0' ]

setuptools.setup(
    name="pds_github_util", # Replace with your own package name
    version=version,
    license="apache-2.0",
    author="thomas loubrieu",
    author_email="loubrieu@jpl.nasa.gov",
    description="util functions for software life cycle enforcement on github",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NASA-PDS/pds-github-util",
    download_url = f"https://github.com/NASA-PDS/pds-github-util/releases/download/{version}/pds_github_util-{version}.tar.gz",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data = {
        '' : ['*.template', 'gh_pages/resources/*', 'gh_pages/resources/images/*']},
    keywords=['github', 'action', 'github action', 'snapshot', 'release', 'maven'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=pip_requirements,
    entry_points={
        # snapshot-release for backward compatibility
        'console_scripts': ['snapshot-release=pds_github_util.release.maven_release:main',
                            'maven-snapshot-release=pds_github_util.release.maven_release:main',
                            'python-snapshot-release=pds_github_util.release.python_release:main',
                            'maven-release=pds_github_util.release.maven_release:main',
                            'python-release=pds_github_util.release.python_release:main',
                            'requirement-report=pds_github_util.requirements.generate_requirements:main',
                            'git-ping=pds_github_util.branches.git_ping:main',
                            'summaries=pds_github_util.gh_pages.build_summaries:main',
                            'pds4-validate=pds_github_util.utils.pds4_validate:main',
                            'ldd-gen=pds_github_util.utils.ldd_gen:main',
                            'ldd-release=pds_github_util.release.ldd_release:main',
                            'release-plan=pds_github_util.plan.plan:main'
                            ],
    },


)
