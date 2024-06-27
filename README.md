# acl_to_arxiv
Scripts to submit a paper using ACL template, including anthology.bib, to arxiv.

## Steps

0. Download your source from Overleaf.

1. Install the [arxiv-latex-cleaner_tool](https://github.com/google-research/arxiv-latex-cleaner). E.g. `pip3 arxiv-latex-cleaner`.

2. Make sure to adjust the `cleaner_config.yaml`
   
3. Edit the first three lines of `run.sh`:
```bash
dirname="path/to/your/source/dir"
dirname_arxiv="${dirname}_arXiv"
main_tex_file="name_of_your_main_tex_file"
```
