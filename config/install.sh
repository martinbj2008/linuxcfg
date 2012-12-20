CFG_ROOT=`pwd`

#configure vim git
cd ~ \
	&& ln -s $CFG_ROOT/git/gitconfig .gitconfig			\
	&& ln -s $CFG_ROOT/git/gitcommit_template .gitcommit_template	\
	&& ln -s $CFG_ROOT/vimrc .vimrc					\
	&& ln -s $CFG_ROOT/vim .vim					\
	&& cd -

#configure bashrc
grep junwei.bashrc ~/.bashrc || \
	echo -e "# User specific aliases and functions \r. $CFG_ROOT/junwei.bashrc" >> ~/.bashrc
