# -*- coding: utf-8 -*-
from binascii import b2a_hex, a2b_hex
import tea ,struct
import md5
key = md5.new(md5.new("python").digest()).digest()
key1='E87B1ED5BF02A8169FBABB701311D8F2'
key2='Kr9kxuztjSgWxNcx'
print b2a_hex(key)
data='66BBA5CF7FFA17A96536C30ED4F24A671A6C17807413B8E83E7B3297C984FB87'

data2=a2b_hex('1097099d1c69f1f5000bb9a7db8526ea1f4000090d511097099d1c69f1f5fe050ba13d89e33b26348aa00a9a5c42000b268c42df69fe0048000000010100f9000174657366736466200009000000008602cbcecce50d')
print struct.unpack('>IIII',data2[:16])
test=(tea.decrypt(a2b_hex(data),key2))
print b2a_hex(test)