from distutils.core import setup
setup(
    name='mann',
    packages=['mann'],  # this must be the same as the name above
    version='0.0.1',
    description='Agent-based model framework for learning',
    author='Daniel Chen',
    author_email='chend@vbi.vt.edu',
    # use the URL to the github repo
    url='https://github.com/chendaniely/multi-agent-neural-network',
    # I'll explain this in a second
    download_url='https://github.com/chendaniely/multi-agent-neural-network/\
                  tarball/0.0.1',
    # arbitrary keywords
    keywords=['agent-based model', 'abm', 'neural network', 'learning',
              'diffusion'],
    classifiers=[],
)
