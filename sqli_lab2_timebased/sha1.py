import hashlib

txt = "bee"
sha1_hash = hashlib.sha1(txt).hexdigest()
print(f"hash: {sha1_hash}")
