import re
import urllib.request
import urllib.parse

def removeHtmlTags(input):
    reg = re.compile('<.*?>')
    output = re.sub(reg, '', input)
    reg = re.compile(r'\\n?')
    output = re.sub(reg, '', output)
    reg = re.compile(r'&(.*?);(.*?);')
    output = re.sub(reg, '', output)
    return output

def main():
    url = 'https://en.wikipedia.org/wiki/1984_in_film'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    # first table is always the top 10 movie list
    tmp = re.findall(r'<td>(.*?)</td>',str(respData))
    movieList = []

    # count to get the first 10 movies
    count = 0
    for result in tmp:
        if "<i>" in result: # each top 10 movie is in italic that's what we use
            movie = []
            movie.append(re.findall(r'<a.*?>(.*?)</a>',result)[0])
            movie.append(re.findall(r'href="(.*?)"',result)[0])
            movieList.append(movie)
            count+=1
        if count == 10: # 10 movies if so
            break

    for movie in movieList:
        print(movie[0])
        urlMovie = 'https://en.wikipedia.org' + movie[1]
        reqMovie = urllib.request.Request(urlMovie)
        respMovie = urllib.request.urlopen(reqMovie)
        MovieData = respMovie.read()
        MovieTmpDesc = re.findall(r'<p>(.*?)</p>',str(MovieData))[0]
        print(removeHtmlTags(MovieTmpDesc))
        print()

if __name__ == "__main__":
    main()