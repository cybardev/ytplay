#!/usr/bin/env python3
# cython: language_level=3
"""
Script to play media from YouTube
"""
# required imports
from urllib import request
from urllib import parse
import getopt
import sys
import os
import re


def error_msg(err_code=0):
    """
    Show an error message and exit with requested error code
    """
    print("ytplay [-v] <search-query>")
    sys.exit(err_code)


def get_media_url(search_str="rickroll", result=0):
    """
    Function to get media URL
    """
    # format the given search string for use in URLs
    query_string = parse.urlencode({"search_query": search_str})
    # get the YouTube search-result page for given search string
    html_content = (
        request.urlopen("https://www.youtube.com/results?" + query_string)
        .read()
        .decode()
    )
    # find the list of video IDs from result page
    search_results = re.findall(r'"videoId":"(.{11})"', html_content)
    # select the first (or given) result and deduce its URL
    media_url = "https://www.youtube.com/watch?v=" + search_results[result]
    # return the URL of requested media
    return media_url


def play(options, search_str, player="mpv"):
    """
    Call the media player and play requested media
    """
    os.system(f"{player} {options} {get_media_url(search_str)}")


def main():
    """
    Main program logic
    """
    # parse flags and arguments
    try:
        opts, extras = getopt.getopt(sys.argv[1:], "hv:")

        # decide whether to play video or audio only for the session
        try:
            if "-h" in opts[0]:
                error_msg()  # show help and exit normally
            elif "-v" in opts[0]:
                # prepare to play video with default quality
                req_search = opts[0][1] + " ".join(extras).rstrip()
                flags = ""
        # when no flags are given...
        except IndexError:
            # and no arguments are given...
            if len(extras) == 0:
                error_msg(2)  # show help and exit with error code 2
            # but if arguments are given,
            # prepare to play audio with best quality
            flags = "--ytdl-format=bestaudio --no-video"
            req_search = " ".join(extras).strip()
    # if invalid flags are used...
    except getopt.GetoptError:
        print("ytplay [-v] <search-query>")
        sys.exit(2)

    # play the requested item and loop over input
    while req_search != "q":
        # call the mpv media player with processed flags and URL
        play(flags, req_search)
        # when done, ask if user wants to repeat the last played media
        answer = input("Repeat? (y/n): ")
        # process user request
        if answer.lower() == "n":
            # if user answers no,
            # ask what to play next, or quit
            req_search = input("Play next (q to quit): ")
        elif answer.lower() == "y":
            # if user answers yes,
            # keep playing
            continue
        else:
            # if invalid option is chosen
            # exit with code 2
            sys.exit(2)
    # exit normally when everything is done
    sys.exit()


# when invoked as a program...
if __name__ == "__main__":
    # execute the main function and process flags and arguments accordingly
    main()
