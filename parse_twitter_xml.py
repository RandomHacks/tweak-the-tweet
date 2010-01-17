#!/usr/bin/python

#from xml.etree import ELementTree as ET
import xml.dom.minidom
import re


def readXmlDoc(name="/tmp/doc.xml"):
    return xml.dom.minidom.parse(name)


file = "offering.xml"

xmldoc = readXmlDoc(file)

loctag = re.compile('#(loc|location)')



def parseCrisisSyntax(line) :
    """
    takes a line of text in Epic Crisis Syntax (tweaked tweet) syntax, and returns a hash table (dictionary)
    of pertinent data
    """
    #line = "#haiti #need #volunteers #loc PAP airport to US #contact 3124988162 #if injured and can travel call in next 5 min #source @carelpedre"

    tagRe = re.compile("#(\w+)")     # generic hashtag regex
    arg_tags = ["loc", "location", "need", "offering", "loc", "location", "contact", "if", "num", "number", "source"]   # hashtags that take arguments
    tagdata = dict() # our output

    tokens = line.split()  # array of our whitespace separated tokens
    cat_arg = False        # variable indicating
    tag = ""


    #iterate over tokens
    for token in tokens:

        if (cat_arg) :
            # we encountered a hashtag that takes arguments, so we will append / conCATenate onto the value in the table
            if not tag in tagdata :
                tagdata[tag] = token
                if (tagRe.match(token)) : 
                    # this token is a hashtag, so don't concatenate any more
                    cat_arg = False
                    continue

            else :
                if (tagRe.match(token)) : 
                    pass
                    cat_arg = False
                else : 
                    tagdata[tag] += " " + token

        m = tagRe.match(token)
        if m :
          # this token is tag
          tag = m.group(1)

          if (tag in arg_tags) :
            # this tag requires arguments turn on concatenation
            cat_arg = True
          else :
            # this is a hashtag w/o arguments just put it in the table
            tagdata[tag] =''
            # turn off concatenation
            cat_arg = False

    for k, v in tagdata.items() :
        print k, ":", v

    return tagdata
            
            


  
line = "RT @sophiabliu Hope for Haiti #haiti #offering #supplies #food #meds #translators #contact Les or Mike 509 3855-1779 / 3663-7197 / 3854-3034"
line = "RT @RIElliot #Haiti #offering #medical #hospitals Hospitals still standing &amp; ready 4 patients in Haiti, http://bit.ly/6dAtl1 via @carelpedre<"
line = "RT @RIElliott: #Haiti #offering full-service hospital not being utilized #location MILOT Haiti  #Name Hopital Sacre Coeur Contact Carol  ..."
line = "#haiti #offering #transport #loc PAP airport to US #contact 3124988162 #if injured and can travel call in next 5 min #source @carelpedre"
#line = "#haiti #need #volunteers #loc PAP airport to US #contact 3124988162 #if injured and can travel call in next 5 min #source @carelpedre"

parseCrisisSyntax(line)


"""
# get all feed tags (should only be one)
feedNodes = xmldoc.getElementsByTagName("feed")

# iterate over <entry>'s in <feed>
for entryElem in feedNodes :
    titleNodes = entryElem.getElementsByTagName("title")

    for titleElem in titleNodes:
       for n in titleElem.childNodes :
            syntax = CrisisSyntax()
            title = n.data
            print title
            syntax.parse(title)

"""
