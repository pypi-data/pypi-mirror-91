# -*- coding: utf-8 -*-
import re

# ‘’‚‛“”„‟« » ====> '", 
#"	&quot;	&#34;	\0022	U+0022	Quotation Mark
#'	&apos;	&#39;	\0027	U+0027	Apostrophe
#«	&laquo;	&#171;	\00AB	U+00AB	Left-Pointing Double Angle Quotation Mark
#»	&raquo;	&#187;	\00BB	U+00BB	Right-Pointing Double Angle Quotation Mark
#‘	&lsquo;	&#8216;	\2018	U+2018	Left Single Quotation Mark
#’	&rsquo;	&#8217;	\2019	U+2019	Right Single Quotation Mark
#‚	&sbquo;	&#8218;	\201A	U+201A	Single Low-9 Quotation Mark
#“	&ldquo;	&#8220;	\201C	U+201C	Left Double Quotation Mark
#”	&rdquo;	&#8221;	\201D	U+201D	Right Double Quotation Mark
#„	&bdquo;	&#8222;	\201E	U+201E	Double Low-9 Quotation Mark
#‹	&lsaquo;	&#8249;	\2039	U+2039	Single Left-Pointing Angle Quotation Mark
#›	&rsaquo;	&#8250;	\203A	U+203A	Single Right-Pointing Angle Quotation Mark

#«U+00AB
#‹U+2039
#»U+00BB
#›U+203A
#„U+201E
#“U+201C
#‟U+201F
#”U+201D
#’U+2019
#"U+0022
#❝U+275D
#❞U+275E
#❮U+276E
#❯U+276F
#⹂U+2E42
#〝U+301D
#〞U+301E
#〟U+301F
#＂U+FF02
#‚U+201A
#‘U+2018
#‛U+201B
#❛U+275B
#❜U+275C
#❟U+275F


regex = re.compile("[ ,.?:;()]+|(?='(?:[^t]|$))")

re_apost = re.compile(r"(?<=\w)[’'](?=\w)")
re_token = re.compile(r"(-?\d+(?:[.,]\d+)*|(?<=\w)['’]\w+|\w+(?:['’]t)?)")
re_token2 = re.compile(r"-?\d+(?:[.,]\d+)*|(?<=\w)['’]\w+|\w+")
trans_quote = str.maketrans("'‘‛’‚“”‟„«»",'"""""""""""')

def call(s):
    words = []
    puncts = []
    punct = ''
    for token in re_token.split(s):
        token = token.strip()
        if token:
            if len(token)>1 and token[0] in "'’-" and token[1].isalnum() or token[0].isalnum():
                words.append(token.replace('\x01',"'"))
                puncts.append(punct)
                punct = ''
            else:
                punct = token.replace(' ','')
    words.append('$')
    puncts.append(punct)

    #return [token.replace("\f","'").replace(" ","") for token in re_token.split(s) if token != '' and not token.isspace()]
    return " ".join("*".join(item) for item in zip(puncts,words))

#def call(s):
#    s = re_apost.sub(" \x01",s)
#    print(s)
#    words = []
#    puncts = []
#    punct = ''
#    for token in re_token.split(s):
#        token = token.strip()
#        if token:
#            if token[0] in "\x01-" or token[0].isalnum():
#                words.append(token.replace('\x01',"'"))
#                puncts.append(punct)
#                punct = ''
#            else:
#                punct = token.replace(' ','')
#    words.append('$')
#    puncts.append(punct)

#    #return [token.replace("\f","'").replace(" ","") for token in re_token.split(s) if token != '' and not token.isspace()]
#    return " ".join("*".join(item) for item in zip(puncts,words))

sents = [
    r'''"It's well-known", she said.''', 
    "'It's over 50,000,000', she said.", 
    "‛It’s over 50.5’, she said.", 
    "‛It’s over -50.5‚, she said.",
    "pair’s",
    "‟It's over”, she said.", 
    "‟It's over„, she said.", 
    "«It isn't over», she said.",
]
for sent in sents:
    #x = call(sent)
    lst = re_token.split(sent)
    lst.append('$')
    lst2 = [(lst[i],lst[i+1]) for i in range(0,len(lst),2)]
    print()
    x = "|".join("/".join(item) for item in lst2)
    print(sent,"===>",x)