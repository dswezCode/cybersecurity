import base64
import hashlib
with open("pass.txt", "r") as input , open('ep.txt', 'w') as output:
    for line in input:
        password = line.strip()
        hash_password = hashlib.md5(password.encode()).hexdigest()
        carlos_hash_password = f"carlos:{hash_password}"
        base64_password = base64.b64encode(carlos_hash_password.encode()).decode()
        output.write(base64_password + "\n")

