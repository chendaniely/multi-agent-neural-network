Multi Agent Neural Network (MANN)
====================

Agent Based Model in Python Using Lens to Compute a Neural Network Decision Making Process

# Setting up LENS
Download LENS: http://web.stanford.edu/group/mbc/LENSManual/index.html

or

https://cmu.app.box.com/s/8dbuauusbm9bamggesv6

#### Ubuntu 14.04 64-bit

Notes from David Plaut: 

> The problem is (was) that the supplied libraries are only for 32-bit machines, which won't link with the 64-bit object files you generate when compiling Lens on a 64-bit machine.

    export LENSDIR=~/code/Lens      # or wherever Lens is installed
    export HOSTTYPE=x86_64-linux    # can set this to more-or-less anything
    cd TclTk/tcl8.3.4/unix
    ./configure --enable-shared --enable-64bit
    make
    rm -f *.o
    cd ../../tk8.3.4/unix
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

If you are re-running <code>./configure</code> remove the config.cache first
    rm config.cache

Finally before running <code>./lens</code> you need to export a few more environment variables

    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LENSDIR}/Bin/${HOSTTYPE}
    export PATH=${PATH}:${LENSDIR}/Bin/${HOSTTYPE}
