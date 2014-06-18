CFG_ROOT=`pwd`

#
git --version || sudo apt-get install git

if [ -d ~/.vim/bundle/vundle ] ; then
	cd ~/.vim/bundle/vundle && git pull && cd -;
else
	git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
fi

#configure vim git
cd ~;
ln -s $CFG_ROOT/git/gitconfig .gitconfig;
#ln -s $CFG_ROOT/git/gitcommit_template .gitcommit_template;
ln -s $CFG_ROOT/vimrc .vimrc;
cd -

#configure bashrc
grep junwei.bashrc ~/.bashrc || \
	(echo  "# User specific aliases and functions" && echo "source $CFG_ROOT/bashrc" )>> ~/.bashrc

#configure terminal tab color
gtkfile="~/.config/gtk-3.0/gtk.css"
if [ -f $gtkfile ] ; then
	grep "TerminalWindow .notebook" $gtkfile || cat gtk.css >> $gtkfile;
else
	mkdir -p ~/.config/gtk-3.0;
	cp -v gtk.css  ~/.config/gtk-3.0/.;
fi
