rsync -rvhcPL bin aldi@$1:~/config/
rsync -rvhcPL lib aldi@$1:~/config/
rsync -rvhcPL .vim aldi@$1:~/config/
rsync -rvhcPL .vimrc aldi@$1:~/config/
rsync -rvhcPL .profile aldi@$1:~/config/
rsync -rvhcPL .bashrc aldi@$1:~/config/
rsync -rvhcPL .git-completion.sh aldi@$1:~/config/
rsync -rvhcPL .gitconfig aldi@$1:~/config/
rsync -rvhcPL .hgrc aldi@$1:~/config/

