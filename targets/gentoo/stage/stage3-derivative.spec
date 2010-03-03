# This file defines common settings for all stage3 derivatives.  Stage3
# derivatives are those targets that are generated directly from a stage3, and
# include stage3-freshen, stage3-quick, stage4 and openvz. A target can be both
# a stage3 generator and a stage3 derivative -- stage3-freshen and stage3-quick
# are two examples.

[section path/mirror]

source: $[:source/subpath]/$[source/name].tar.bz2

[section source]

: stage3
name: $[]-$[:subarch]-$[:version]

# When building from a stage3, we now simply use the stage3 with matching
# build, subarch and version:

build: $[target/build] 
subarch: $[target/subarch]

# For a regular full build, the source/version and target/version will be
# equal. However, for a stage3-freshen build, we will use the last-built
# stage3 as a seed:

version: << $[path/mirror/control]/version/stage3


