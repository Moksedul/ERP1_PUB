value = 2**38
print(value)

txt = "map"

mytable = txt.maketrans("abcdefghijklmnopqrstuvwxyz", "cdefghijklmnopqrstuvwxyzab")

print(txt.translate(mytable))
string = "dfdf" \
         ""
char_seen = []
for char in string:
    if char not in char_seen:
        char_seen.append(char)
print(''.join(char_seen))