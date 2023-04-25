import os

with open("best_recursive_1674759469.txt", "r") as best_file:
    seen = set()
    words = best_file.readline().split(" ")
    previous = ""
    for word in words:
        if previous:
            if word in seen:
                print(f"DUPLICATE: {word}")
                exit()
            if previous[-2:] != word[:2]:
                print(f"WORDS DON'T FIT: {previous} {word}")
                exit()
        seen.add(word)
        previous = word
    print("CORRECT")
