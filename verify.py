import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "best_recursive_1683119746.txt"

with open(filename, "r") as best_file:
    seen = set()
    words = best_file.readline().split(" ")
    previous = ""
    for word in words:
        if previous and word:
            if word in seen:
                print(f"DUPLICATE: {word}")
                exit()
            if previous[-2:] != word[:2]:
                print(f"WORDS DON'T FIT: {previous} {word}")
                exit()
        seen.add(word)
        previous = word
    print("CORRECT")
