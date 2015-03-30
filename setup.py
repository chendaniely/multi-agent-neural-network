from distutils.core import setup

setup(
    name='mann',
    packages=['mann'],  # this must be the same as the name above
    version='0.0.1',
    description='Multi-Agent Neural-Network',
    author='Daniel Chen',
    author_email='chend@vbi.vt.edu',
    license="MIT",
    url='https://github.com/chendaniely/multi-agent-neural-network',
    download_url='https://github.com/chendaniely/multi-agent-neural-network/\
                  tarball/0.0.1',
    keywords=['agent-based model', 'abm', 'neural network', 'learning',
              'diffusion'],
    scripts=['mann/agent.py',
             'mann/network_agent.py',
             'mann/network.py'],
    classifiers=['Natural Language :: English', ],
    long_description='README.md',
)
