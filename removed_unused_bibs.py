"""
Original code from: https://gist.github.com/TomWagg/d3c6abf4a3663c8f0770a106063240d9

>>> python remove_unused_bibs.py -h
usage: remove_unused_bibs.py [-h] [-b BIB_FILES] [-p PAPER_FILES] [-o OUT_FILE]
Remove unused bibtex entries
options:
  -h, --help            show this help message and exit
  -b BIB_FILES, --bib_files BIB_FILES
      Comma-separated list of bib files (default: paper.bib)
  -p PAPER_FILES, --paper_files PAPER_FILES
      Comma-separated list of paper files (default: paper.tex)
  -o OUT_FILE, --out_file OUT_FILE
      Output path for the minimal bib file (default: min.bib)
"""

import re
import argparse

def collect_all_bibs(bib_files):
    # regex for anything that matches "@[some word]{[something],"
    bibtex_key_regex = r"@\w*{.*(?=\,)"

    # convert strings to lists in case only one file
    if isinstance(bib_files, str):
        bib_files = [bib_files]

    # track the combined bib file as a string
    all_bib_string = ""
    all_keys = []

    # read in each bib file
    for file in bib_files:
        with open(file, "r") as f:
            bib_string = f.read()
            all_bib_string += bib_string

            # find all of the keys that match the regex
            matches = re.findall(pattern=bibtex_key_regex, string=bib_string)

            # trim off the preceding @whatever
            all_keys += [m.split("{")[1] for m in matches]

    # return unique set of keys and entire bib string
    return sorted(list(set(all_keys))), all_bib_string


def check_bibs_used(paper_files, keys):
    tex_regex = r"\\cite.*{.*tom.*}"
    if isinstance(paper_files, str):
        paper_files = [paper_files]

    # track whether each key is ever used
    ever_used = [False for _ in range(len(keys))]
    for file in paper_files:
        with open(file, "r") as f:
            paper_string = f.read()

        # check each key in each file
        for i, key in enumerate(keys):
            # for markdown (JOSS paper) the check is simple
            if file.endswith(".md") and f"@{key}" in paper_string:
                ever_used[i] = True
            # for latex we need to be a little smarter about checking for \cite commands
            elif file.endswith(".tex") and re.search(tex_regex.replace("tom", re.escape(key)), paper_string) is not None:
                ever_used[i] = True
    return ever_used

def isolate_bibtex_entry(s, start):
    # isolate a bibtex entry based on closing curly braces
    braces, cursor, not_opened = 0, start, True
    while braces > 0 or not_opened:
        if s[cursor] == "{":
            braces += 1
            not_opened = False
        elif s[cursor] == "}":
            braces -= 1
        cursor += 1
    return s[start: cursor]

def create_min_bib_file(bib_string, keys, keys_used, out_file):
    min_bib_string = ""

    # keep @strings (useful for ACL Anthology)
    for line in bib_string.split('\n'):
        x = line.strip()
        if x.startswith('@string{'):
            min_bib_string += x + '\n'

    for k, used in zip(keys, keys_used):
        if used:
            key_regex = r"@\w*{" + re.escape(k) + r"(?=\,)"
            match = re.search(key_regex, bib_string)
            min_bib_string += isolate_bibtex_entry(bib_string, match.start()) + "\n\n"
        
    with open(out_file, "w") as f:
        f.write(min_bib_string)


def remove_unused_bibs(bib_files, paper_files, out_file):
    keys, bib_string = collect_all_bibs(bib_files=bib_files)
    keys_used = check_bibs_used(paper_files=paper_files, keys=keys)
    create_min_bib_file(bib_string=bib_string, keys=keys, keys_used=keys_used, out_file=out_file)

def main():
    parser = argparse.ArgumentParser(description='Remove unused bibtex entries',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter) 
    parser.add_argument('-b', '--bib_files', default="paper.bib", type=str,
                        help="Comma-separated list of bib files")
    parser.add_argument('-p', '--paper_files', default="paper.tex", type=str,
                        help="Comma-separated list of paper files")
    parser.add_argument('-o', '--out_file', default="min.bib", type=str,
                        help="Output path for the minimal bib file")
    args = parser.parse_args()

    bib_files = args.bib_files.split(",")
    paper_files = args.paper_files.split(",")

    remove_unused_bibs(bib_files=bib_files, paper_files=paper_files, out_file=args.out_file)

if __name__ == "__main__":
    main()
