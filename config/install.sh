CFG_ROOT=`pwd`

#
git --version || sudo apt-get install git

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

#configure vim git
cd ~ \
	&& ln -s $CFG_ROOT/git/gitconfig .gitconfig			\
	&& ln -s $CFG_ROOT/git/gitcommit_template .gitcommit_template	\
	&& ln -s $CFG_ROOT/vimrc .vimrc					\
	&& ln -s $CFG_ROOT/vim .vim					\
	&& cd -

#configure bashrc
grep junwei.bashrc ~/.bashrc || \
	(echo  "# User specific aliases and functions" && echo "source $CFG_ROOT/bashrc" )>> ~/.bashrc
