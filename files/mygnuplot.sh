#!/bin/sh
# Because !@#$%^ Java can't fucking do this without a bazillion lines of codes.
set -e
stdout=$1
shift
stderr=$1
shift
sed -i 's/set term png small size/set term png size/' $@
exec nice gnuplot "$@" >"$stdout" 2>"$stderr"
