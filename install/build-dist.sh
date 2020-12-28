#!/bin/bash
set -e
ddir=makaronLab
rdir=../build/dist
tdir=$rdir/$ddir
echo "[build-dist] Building folders ..."
mkdir -p $tdir
cp ../build/editor/mLabEditor $tdir/
cp ../install/makaronLab.desktop $tdir/
mkdir -p $tdir/lib/
cp ../build/lib/* $tdir/lib/
mkdir -p $tdir/plugins
cp ../build/plugins/* $tdir/plugins/
mkdir -p $tdir/packages
cp ../packages/* $tdir/packages/
cp ../install/setup.sh $tdir/
cd $rdir && tar -czvf makaronLab.tar.gz $ddir

