#!/usr/bin/python

# Author: Alexander Vencel
# Version: 07/07/19
# File: movie.py
# Purpose: Retrieve the top 10 movies from a year
#          in input, then displaying a small summary
#          of the movie. All the data is retrieved
#          from wikipedia.
# Known issue: Unicode characters are not cleaned
#          before text is displayed on the console

import re
import urllib.request
import urllib.parse
import datetime

# Simple function that cleans the html we retrieved
# in order to display only the text.
def removeHtmlTags(input):
    reg = re.compile('<.*?>')
    output = re.sub(reg, '', input)
    reg = re.compile(r'\\n?')
    output = re.sub(reg, '', output)
    reg = re.compile(r'&(.*?);(.*?);')
    output = re.sub(reg, '', output)
    return output

def main():
    print("------------------------------------------------------")
    print("               WIKI MOVIE RETRIEVER"                   )
    print("                  By Alex Vencel"                      )
    print("                 Version: 07/07/19"                    )
    print("------------------------------------------------------")
    
    now = datetime.datetime.now()
    thisYear = int(now.year)

    runProg = 'Y'
    while(runProg=='Y'):
        # input year and check if valid
        year = 0
        while year < 1920 or year > thisYear:
            year = input("\nEnter a year (from 1920 to this day): ")
            try:
                year = int(year)
                if year < 1920 or year > thisYear:
                    print("Sorry, that year is not int the range")
            except ValueError:
                print("That's not a number...")
                year = 0

        # retrieving the 10 movies for the inputed year
        url = 'https://en.wikipedia.org/wiki/' + str(year) + '_in_film'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        tmp = re.findall(r'<td>(.*?)</td>',str(respData)) # first table is always the top 10 movie list
        movieList = []
        count = 0 # count to get the first 10 movies
        for result in tmp:
            if "<i>" in result: # each top 10 movie is in italic that's what we use
                movie = []
                movie.append(re.findall(r'<a.*?>(.*?)</a>',result)[0])
                movie.append(re.findall(r'href="(.*?)"',result)[0])
                movieList.append(movie)
                count+=1
            if count == 10:
                break

        # we have the 10 movies and their wiki link
        # for each we navigate to the link and retrieve 1st paragraph (small summary)
        count=1
        for movie in movieList:
            print("\n"+ str(count) + "). " + movie[0])
            count+=1
            urlMovie = 'https://en.wikipedia.org' + movie[1]
            reqMovie = urllib.request.Request(urlMovie)
            respMovie = urllib.request.urlopen(reqMovie)
            MovieData = respMovie.read()
            MovieTmpDesc = re.findall(r'<p>(.*?)</p>',str(MovieData))[0]
            print(removeHtmlTags(MovieTmpDesc))
            print("------------------------------------------------------")

        # continue again ?
        runProg = ''
        while runProg != 'Y' and runProg != 'N':
            runProg = input("\nWould you like to continue (Y/n)? ").upper()

if __name__ == "__main__":
    main()