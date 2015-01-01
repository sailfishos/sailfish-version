#!/bin/bash
#
# Outside of starting a new release cycle the version number needs to remain
# intact, and only revisions increased/added. This script helps automating
# that.

OLDTAG=`git describe --tags 2>/dev/null`

if [ -n "$OLDTAG" ]; then
    NEWTAG=`echo $OLDTAG | awk -f tag.awk`
fi

echo -n "New tag (default: $NEWTAG): "
read readtag

if [ -n "$readtag" ]; then
    NEWTAG=$readtag
fi

if [ -z "$NEWTAG" ]; then
    echo "No valid tag"
    exit 1
fi

git tag $NEWTAG
git push --tags
