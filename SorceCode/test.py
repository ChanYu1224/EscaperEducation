n = int(input())
s = list(input())

s_len = len(s) #文字列の長さを取得

for i in range(s_len): #文字列処理
  tmp = ord(s[i]) + n
  if tmp > ord('Z'):
    tmp -= 26
  s[i] = chr(tmp)

print("".join(s)) #文字列出力