#!/bin/sh
# Auto checkout the needed tags used by current components($1)
 
rbb_tag=$1
prefix=$2

function checkout_tag {
	git_url=$1
	git_tag=$2

	[ "X$git_tag" == "X" ] && (echo "Warning: faile get tag from arg[$1]"; return)

	dst_dir="$prefix/aston/h_debit/deliveries/$git_url"
	mkdir -p $dst_dir
	if [ -d $dst_dir/$git_tag ] ; then
		echo "Skip $dst_dir/$git_tag"
		return
	else
		echo "checkout   $git_tag to $dst_dir"
		git_repo="$prefix/aston/h_debit/scm/git/projects/$git_url.git"
		git archive --format=tar --prefix=$git_tag/ $git_tag --remote=$git_repo | (cd $dst_dir && tar xvf -)
	fi
}

echo "------------- Start ---------------------------"
date
echo
[ "X$rbb_tag" == "X" ] && rbb_tag="HEAD"

git archive --format=tar $rbb_tag --remote=$prefix/aston/h_debit/scm/git/projects/framework/components.git components.config | tar xf  - -O | \
  grep -v ^# | grep -v \= | grep -v kernels |grep -v snapgear | grep -v $^ | while read line;
do
	[ "X$line" == "X" ] || checkout_tag $line
done
echo 
date
echo 
echo "Auto checkout finish"
echo "----------------------------------------"
