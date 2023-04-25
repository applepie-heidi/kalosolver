import time
from collections import defaultdict

started = time.time()


def parse_groups(filename):
    groups = defaultdict(lambda: [])

    with open(filename, "r") as words_f:
        lines = words_f.readlines()
        prefixes = {}

        for word in lines:
            word = word[:-1]
            if not (word.startswith("ka") and word != "kalodont"):
                prefix = word[:2]
                suffix = word[-2:]
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                group = prefix + suffix
                groups[group].append(word)

        for group in list(groups):
            prefix = group[:2]
            suffix = group[-2:]
            if suffix not in prefixes or (prefix == suffix and prefixes.get(suffix, 0) == 1):
                del groups[group]
    return groups


def main():
    groups = parse_groups("rijeci.txt")

    with open("groups_wc.txt", "w") as groups_wc_f:
        for group, words in sorted(groups.items()):
            wlist = ','.join(words)
            groups_wc_f.write(f"{group},{len(words)},{wlist}\n")


if __name__ == '__main__':
    main()
