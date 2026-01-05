print("[", end="")

with open("pass.txt", "r") as passwords:
    for line in passwords:
        password = line.strip()
        print(f'"{password}",', end="")
    print('"random"]')

       