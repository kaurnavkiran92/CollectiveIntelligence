import feedparser
import re
import pprint

# Returns title and dictionary of word counts for an RSS feed

def getwordcounts(url):
    print "getwordcounts func"
    # Parse the feed
    d = feedparser.parse(url)

    wc = {}

    try:
        pprint.pprint( d['feed']['title'] )
    except KeyError:
        print url , " is not RSS."

    print 'a'
#    pprint.pprint(d.feed.style)
#    pprint.pprint(d.feed.links)
#    pprint.pprint(d.feed.script)
#    pprint.pprint(d.feed.summary)
#    pprint.pprint(d.feed.html)
#    pprint.pprint(d.feed.meta)

    # Loop over all the entries
    for e in d.entries:

        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # Extract a list of words
        words = getwords(e.title + ' ' + summary)

        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed['title'], wc

def getwords(html):
    print "getWords func"
    # Remove all the HTML tags
    rcmp = re.compile(r'<[^>]+>')
    txt = rcmp.sub('',html)
    
    # Split words
    rcmp = re.compile(r'[^A-Z^a-z]+')
    words = rcmp.split(txt)

    # Convert to lowercase
    buffer = [word.lower() for word in words if word != '']
    return buffer

def main():
    apcount = {}
    wordcounts = {}
    feedlist = [line for line in file('feedlist.txt')]
        
    for feedurl in file('feedlist.txt'):
        try:
            title , wc = getwordcounts(feedurl)
            wordcounts[title] = wc
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1
        except:
            pass

    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if frac > 0.1 and frac < 0.5 :
            wordlist.append(w)

    out = file('blogdata.txt', 'w')
    out.write('Blog')

    for word in wordlist:
        out.write('\t%s' % word)

    out.write('\n')

    for blog, wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
        out.write('\n')

if __name__ == "__main__":
    main()
