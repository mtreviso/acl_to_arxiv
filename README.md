# acl_to_arxiv
Scripts to submit a paper using ACL template, including anthology.bib, to arxiv. 

These scripts will clean out all comments and pre-specified macros, and will reduce the size of anthology.bib by filtering out unused references.

A new folder with the suffix "_arXiv" will be created, which can be zipped and uploaded to arxiv.


## Steps

0. Download your source from Overleaf

2. Install the [arxiv-latex-cleaner_tool](https://github.com/google-research/arxiv-latex-cleaner):

   ```
   pip3 arxiv-latex-cleaner
   ```

3. Make sure to adjust the `cleaner_config.yaml`:

   - Add the macros you want to delete to `commands_to_delete`
   

4. Edit the first three lines of `run.sh`:

```bash
dirname="path/to/your/source/dir"
dirname_arxiv="${dirname}_arXiv"
main_tex_file="name_of_your_main_tex_file"
```

   - Then run it via `bash run.sh`

5. Download the `output.bbl` from Overleaf, and move it to `${dirname}_arXiv` with the name `main.bbl`

6. Zip the directory `${dirname}_arXiv` and upload it to arxiv.
 
