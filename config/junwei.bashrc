# junwei's .bashrc append 

# User specific aliases and functions
#junwei tools
function sgcheckout() {
	dst_dir=$1
	if [ "X$dst_dir" == "X" ] ; then

		dst_dir="sg"
	fi
	if [ -f components.config ]; then
		cd ..;
	elif ! [ -f components/components.config ]; then
		echo "Error!! NOT find components.config !!!! "
		return 1;
	fi
	echo "Use components/components.config to checkout snapgear ===> $dst_dir"
	./components/checkout.sh  -d $dst_dir framework/snapgear && cd $dst_dir
}

#6Wind make commands
alias makek34='use_x86_64-gcc-4.4.6-eglibc-2.15; make autoconfig CONFIG_FP_IMPLEMENTATION=FP-NONE \
	CONFIG_HA=n CONFIG_PRODUCT=PC-X86_64 CONFIG_KERNEL=linux-2.6-k2.6.34 \ 
	CONFIG_LIBC=eglibc-2-15-gcc-4.4.6 CONFIG_ROOTFS=initramfs CONFIG_DPDK='

alias makexlp='use_broadcom_sdk_2_2_4_toolchain; make autoconfig CONFIG_FP_IMPLEMENTATION=FP-MCEE \
	CONFIG_HA=n CONFIG_PRODUCT=XLP CONFIG_KERNEL=linux-2.6-broadcom-sdk-2.2.4 \
	CONFIG_LIBC=libc-broadcom-2.2.4-n64 CONFIG_ROOTFS=initramfs'

alias makeoctean2_3='make autoconfig CONFIG_FP_IMPLEMENTATION=FP-MCEE \
	CONFIG_HA=n CONFIG_PRODUCT=OCTEON2 CONFIG_KERNEL=linux-2.6-octeon-sdk2.3 \
	CONFIG_LIBC=libc-cv-sdk2.3-n64 CONFIG_ROOTFS=initramfs'

alias apollo='ssh h_debit@apollo'
alias artemis='ssh h_debit@artemis'
alias pandora='ssh h_debit@pandora'
alias shanghai='ssh h_debit@shanghai'
alias tianjin='ssh h_debit@tianjin'
alias avatar='ssh avatar'
alias wukong='ssh h_debit@wukong'
alias bajie='ssh h_debit@bajie'
alias caviumhost1='ssh h_debit@caviumhost1'
alias caviumhost2='ssh h_debit@caviumhost2'
alias stand='ssh h_debit@stand'
alias alone='ssh h_debit@alone'
alias lion='ssh h_debit@lion'
alias tiger='ssh h_debit@tiger'
alias tamarillo='ssh h_debit@tamarillo'
alias pepino='ssh h_debit@pepino'
alias puma='ssh h_debit@puma'
alias demonicus='ssh h_debit@demonicus'
alias willow='ssh h_debit@willow'
alias poplar='ssh h_debit@poplar'
alias oak='ssh h_debit@oak'
alias larch='ssh h_debit@larch'
alias cedar='ssh h_debit@cedar'
alias sequoia='ssh h_debit@sequoia'
alias glacon='ssh h_debit@glacon'
alias palm='ssh h_debit@palm'
alias yeti='ssh h_debit@yeti'
alias lucky='ssh h_debit@lucky'
alias cobra3='ssh h_debit@cobra3'
alias cobra='ssh h_debit@cobra'
alias cobra2='ssh h_debit@cobra2'
alias benjamin='ssh h_debit@benjamin'
alias baobab='ssh h_debit@baobab'
alias quake='ssh h_debit@quake'
alias ken='ssh h_debit@ken'
alias agaric='ssh h_debit@agaric'
alias junweiagaric='ssh junwei@agaric'

#targets
alias lasa='ssh h_debit@shanghai -t tip lasa'
alias xian='ssh h_debit@shanghai -t tip xian'

alias taibei='ssh h_debit@tianjin -t tip taibei'
alias aomen='ssh h_debit@tianjin -t tip aomen'

alias green='ssh h_debit@tianjin -t tip green'
alias yellow='ssh h_debit@tianjin -t tip yellow'

alias toyota='ssh h_debit@artemis -t tip toyota'
alias honda='ssh h_debit@artemis -t tip honda'


alias watermeloon='ssh h_debit@wukong -t tip watermelon'
alias coconut='ssh h_debit@wukong -t tip coconut'

alias grape='ssh h_debit@wukong -t tip grape'
alias test='ssh h_debit@bajie -t tip test'
alias slime='ssh root@10.81.0.193 -t cu -l /dev/ttyS4a'

#XLP
alias bronson='ssh h_debit@willow -t tip bronson'
alias simone='ssh cobra -lh_debit -t bin/tip.sh simone'
alias yves='ssh h_debit@cobra -t bin/tip.sh yves'
alias robinson='ssh h_debit@willow -t tip robinson'
alias autobench_tiger='ssh -p5022 h_debit@tiger'

#pp81:
alias tequila='ssh root@10.81.0.181 -t cu -l /dev/ttyS2a'
alias paf='ssh root@10.81.0.181 -t cu -l /dev/ttyS4a'
alias kfar='ssh root@10.81.0.175 -t cu -l /dev/ttyS2a'
alias blat='ssh root@10.81.0.175 -t cu -l /dev/ttyS4a'
alias thym='ssh root@10.81.0.64 -t cu -l /dev/ttyS2a'
alias lavande='ssh root@10.81.0.64 -t cu -l /dev/ttyS4a'

alias grep='grep --color '

#log as junwei
alias junweilion='ssh lion' 
alias junweitiger='ssh tiger' 
alias junweipuma='ssh puma' 
alias junweilucky='ssh lucky' 

#pr list
alias prlist='ssh lion /home/junwei/script/pr.py'
alias checkpatch='/home/junwei/git/linux-generic-2.6.34/scripts/checkpatch.pl'