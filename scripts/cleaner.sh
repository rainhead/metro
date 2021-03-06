#!/bin/bash

mirrpath=`metro -k path/mirror`

cd $mirrpath || exit 1

zapme=""

# find stage1's that have been around more than 24 hours with no corresponding stage3, and add parent dir to wipe list

for x in `find -mtime +0 -iname stage1*.tar.bz2`
do
	if ! [ -e `dirname $x`/stage3*.tar.bz2 ]
	then
		zapme="$zapme `dirname $x`"
	fi
done

# only keep the 3 most recent stage3 dirs - any older than that are added to our wipe list

for x in `ls -d */* | grep -v snapshots`
do
	numstage3s=`find $x -iname stage3*.tar.bz2 | grep -v "current.tar.bz2" | wc -l`
	numtozap=$(( $numstage3s - 3 ))
	if [ $numtozap -le 0 ]
	then
		continue
	fi
	for y in `find $x -iname stage3*.tar.bz2 | grep -v "current.tar.bz2" | sort -r | tail -n $numtozap`
	do
		dirtozap=`dirname $y`
		zapme="$zapme $dirtozap"
	done
done
	
# also remove empty build directories

for x in `ls -d */* | grep -v snapshots`
do

	for y in `ls -d ${x}/*`
	do
		if [ -d $y ] && [ "`ls $y | wc -l`" = "0" ]
		then
			zapme="$zapme $y"
		fi
	done
done

# keep only the last 7 portage snapshots - any older than that are added to our wipe list

for build in gentoo funtoo ~funtoo
do
	[ -d $build ] || continue
	numsnaps=`ls -d $build/snapshots/* | grep -v "current.tar.bz2" | wc -l`
	numtozap=$(( $numsnaps - 7 ))
	if [ $numtozap -le 0 ]
	then
		continue
	fi
	for x in `ls -d $build/snapshots/* | grep -v "current.tar.bz2" | sort -r | tail -n $numtozap`
	do
		zapme="$zapme $x"
	done
done

mbs=0

# actually remove the stale directories and calculate total MB removed

for x in $zapme
do
	dirmb=`du -m --max-depth=0 $x | cut -f1`
	mbs=$(( $mbs + $dirmb ))
	echo $x
	rm -rf $x
done
if [ "$zapme" != "" ]
then
	echo "$mbs MB total removed"
fi
