# #Q.1
# name=str(input("Enter your name:")) # if str is not written also fine 
# print(f"good morning,{name}")

#Q.2
letter='''Dear <|Name|>,
You are selected!
<|Date|>'''

print(letter.replace("<|Name|>","shreetej").replace("<|Date|>","24 August"))

#Q.3
x="Shreetej is good  boy"
print(x.find("  ")) # double space is at 16 place and using this func we can also find any word or letter in str

y=(x.replace("  "," "))
print(y)

#after this even if we print(name) that original string will not change,cause strings are immutable