from sretools import SimpleTable
import re


tbl = list()
hdr = re.split(r",","id,名字name,定义definition,备注comment")

r1 = [1,"views","select * from 哈哈大学tables abc ass  asdf   asdf   asdf   asdf\n wherexx卡卡卡卡 type = 'V' \n order by 1","test\ntest\ntest"]
r2 = [2,"functions","select * from functions\n order xixiha嘻嘻哈哈by 1 asd haha haha haha xx x","test\ntest\ntest"]

tbl.append(r1)
tbl.append(r2)

print(SimpleTable(data=tbl,header=hdr,maxwidth=30))



