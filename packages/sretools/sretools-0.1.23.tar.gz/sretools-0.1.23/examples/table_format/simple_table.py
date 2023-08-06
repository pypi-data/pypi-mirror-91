from sretools import SimpleTable

hdr=["h1","h2","h3","h4"]
dat = [
        ["a","b","cc","d"],
        ["1","xx","xxcc","d"],
        ["55","  xx","","d"],
        ["","  xx","aa bb  cc","d"],
        ]


st = SimpleTable(header=hdr,data=dat)
print(st)


#  [yonghang@xsvr]$ python3 simple_table.py
#  h1 h2   h3        h4
#  --------------------
#  a  b    cc        d
#  1  xx   xxcc      d
#  55   xx           d
#       xx aa bb  cc d

#  $ cat test.txt
#  a,b,c
#  哈哈大笑,ddasdf,xx
#  dadsf,这是一个故事,xxxabc
#  
#  $ sretools-tblfmt -H "H1,H2,Hthree" -f test.txt -b,
#  H1       H2           Hthree
#  ----------------------------
#  a        b            c
#  哈哈大笑 ddasdf       xx
#  dadsf    这是一个故事 xxxabc
