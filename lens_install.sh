#! /usr/bin/bash

apt-get install libx11-dev
apt-get install tcl8.4-dev tk8.4-dev

cd ~/
mkdir -p code
cd code

wget https://github.com/chendaniely/multi-agent-neural-network/raw/master/Lens.tgz
tar xvzf Lens.tgZ
cd Lens

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

export LENSDIR=~/code/Lens      # or wherever Lens is installed
export HOSTTYPE=x86_64-linux    # same as above during make
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LENSDIR}/Bin/${HOSTTYPE}
export PATH=${PATH}:${LENSDIR}/Bin/${HOSTTYPE}
