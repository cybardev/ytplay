# THIS IS A PERSONAL FORK AND SUBJECT TO RANDOM CHANGES THAT MAY NOT WORK. USE AT YOUR OWN RISK.
### I strongly recommend you to use the original script from [pystardust's repo](https://github.com/pystardust/ytfzf).

## ytplay

A POSIX script that helps you find YouTube videos without needing API keys, and opens/downloads using mpv/youtube-dl.
- History support
- Download support
- Format selection

Initially this used to be a single line script. But for portability and extensibility I am breaking my vow. If you still are here for the memes then use the line below.

```sh
#!/bin/sh
[ -z "$*" ] || curl "https://www.youtube.com/results" -s -G --data-urlencode "search_query=$*" |  pup 'script' | grep  "^ *var ytInitialData" | sed 's/^[^=]*=//g;s/;$//' | jq '..|.videoRenderer?' | sed '/^null$/d' | jq '.title.runs[0].text,.longBylineText.runs[0].text,.shortViewCountText.simpleText,.lengthText.simpleText,.publishedTimeText.simpleText,.videoId'| sed 's/^"//;s/"$//;s/\\"//g' | sed -E -n "s/(.{60}).*/\1/;N;s/\n(.{30}).*/\n\1/;N;N;N;N;s/\n/\t|/g;p" | column -t  -s "$(printf "\t")" | fzf --delimiter='\|' --nth=1,2  | sed -E 's_.*\|([^|]*)$_https://www.youtube.com/watch?v=\1_' | xargs -r -I'{}' mpv {}
```

# Usage

![Gif](ytfzf.gif)

	Usage: ytfzf <search query>
	     -h                    Show this help text
	     -H                    Choose from history
	     -D                    Delete history
	     -m  <search query>    Audio only (for listening to music)
	     -d  <search query>    Download to current directory
	     -f  <search query>    Show available formats before proceeding
	     -a  <search query>    Auto play the first result (no fzf)
         -l  <search query>    loop: prompt again after video ends

* Video to be selected using fzf.
* Searches based on title and channel names.

## Examples
> Watch video

	ytfzf <query>
	
* You can use multiple options together, here are some examples

> Steam audio (music)

	ytfzf -m <query>

> Download a video from your history

	ytfzf -dH

> Download a video in a certain format

	ytfzf -fd  <query>

If you started watching a video and you wish to change format then 
first hit Q to save position and quit mpv, then choose your format using

	ytfzf -fH


# Dependencies
* mpv
* [youtube-dl](https://github.com/ytdl-org/youtube-dl)
* [fzf](https://github.com/junegunn/fzf) - for menu
* [jq](https://github.com/stedolan/jq) - to parse json

### Arch based

	sudo pacman -S jq mpv youtube-dl fzf 

### Debian based

	sudo apt install jq mpv youtube-dl fzf 

> Note youtube-dl is usually outdated in debian repos, I suggest getting it from 

* [youtube-dl github](https://github.com/ytdl-org/youtube-dl)

# Installation

	git clone https://github.com/cybarspace/ytfzf
	cd ytfzf
	chmod +x ytfzf

Copy it to your path
	
	sudo cp ytfzf /usr/local/bin/

Arch users can install ytfzf from the [AUR](https://aur.archlinux.org/packages/ytfzf-git/)
	
	yay -S ytfzf-git
        


# Defaults

These setting can be tweaked from the first section of the script. Edit them as shown below.

### History

On by default. If you don't want history.

	save_history=1                         # 0: history off, 1: history on
	
* File location 

	~/.cache/ytfzf/ytfzf_hst

### Loop prompt

Off by default. Can be turned on using option -f.
* This would return you to the fzf video selection prompt after the video is exited/ends.
* To quit the script you can press ESC or ^C in the fzf video selection prompt.

	prompt_loop=0                          # to prompt again after video finishes

### Currently Playing

On by default. Stores the details of the currently playing track. Empty when nothing is playing. This could be used in status bar modules.

	save_cur=1                             # For status bar modules

* File location 

	~/.cache/ytfzf/ytfzf_hst

# Todo

* Playlists
* Icons
