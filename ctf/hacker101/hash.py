import hashlib
text = "dan"
hashed_text = hashlib.md5(text.encode()).hexdigest()
print(hashed_text)
