[![Build Status](https://travis-ci.org/chendaniely/multi-agent-neural-network.svg?branch=master)](https://travis-ci.org/chendaniely/multi-agent-neural-network)

[![Coverage Status](https://coveralls.io/repos/chendaniely/multi-agent-neural-network/badge.png?branch=master)](https://coveralls.io/r/chendaniely/multi-agent-neural-network?branch=master)

Multi Agent Neural Network (MANN)
====================

Agent Based Model in Python Using Lens to Compute a Neural Network Decision Making Process

# Setting up LENS
Download LENS: http://web.stanford.edu/group/mbc/LENSManual/index.html

or

https://cmu.app.box.com/s/8dbuauusbm9bamggesv6

    wget https://github.com/chendaniely/multi-agent-neural-network/raw/master/Lens.tgz
    wget http://web.stanford.edu/group/mbc/LENSManual/Manual/Dist/lens.tar.gz
    tar xvzf Lens.tgZ

note the older lens link has a capital letter, the one from Stanford has a lower case

#### Ubuntu 14.04 64-bit

Notes from David Plaut: 

> The problem is (was) that the supplied libraries are only for 32-bit machines, which won't link with the 64-bit object files you generate when compiling Lens on a 64-bit machine.

    export LENSDIR=~/code/Lens      # or wherever Lens is installed
    export HOSTTYPE=x86_64-linux    # can set this to more-or-less anything
    cd TclTk/tcl8.3.4/unix
    rm config.cache
    ./configure --enable-shared --enable-64bit
    make
    rm -f *.o
    cd ../../tk8.3.4/unix
    rm config.cache
    ./configure --enable-shared --enable-64bit --with-tcl=../../tcl8.3.4/unix
    # ./configure --enable-shared --enable-64bit --with-tcl=../../tcl8.3.4/unix
    make
    rm -f *.o
    cd $LENSDIR
    mkdir Bin/$HOSTTYPE
    mv TclTk/tcl8.3.4/unix/libtcl8.3.* Bin/${HOSTTYPE}
    mv TclTk/tk8.3.4/unix/libtk8.3.* Bin/${HOSTTYPE}
    cd $LENSDIR
    make all

<code>./configure</code> is failing make sure the follow files have execute permission <code>chmod 775</code>

    - config.status
    - configure
    - configure.in
    - configure.ORIG
    - install-sh
    - ldAix
    - mkLinks
    - tclsh
    - wish
    
or you can `chmod 755 -R` your `Lens` folder

If making the tcl library fails becuase of X11/Xlib.h header file run `apt-get install libx11-dev`

`sudo apt-get install tcl8.4-dev tk8.4-dev`

If you are re-running <code>./configure</code> remove the config.cache first `rm config.cache`

Finally before running <code>./lens</code> you need to export a few more environment variables.  It is best to add these to your .bashrc file

    export LENSDIR=~/code/Lens      # or wherever Lens is installed
    export HOSTTYPE=x86_64-linux    # same as above during make
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LENSDIR}/Bin/${HOSTTYPE}
    export PATH=${PATH}:${LENSDIR}/Bin/${HOSTTYPE}

If you are running Lens on a remote machine via SSH, remember to ssh via <code> ssh -X </code>

If you are planning to run the nose tests:

`nosetests --cover-branches --with-coverage --cover-erase --cover-package=mann`
