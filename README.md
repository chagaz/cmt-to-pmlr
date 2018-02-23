# cmt-to-pmlr
Process CMT files into PMLR proceedings

## Steps to follow for processing files from CMT
1. Download the camera ready papers from CMT. CMT will split the papers in several folders of under 100MB each zipped. Unzip them, and move all the papers in a single repository (e.g. `CameraReadyPapers`)

2. Download the list of papers as a .xls file from CMT. Export it as a .csv file (make sure it contains only accepted papers). Use ',' as a delimiter and '"' as a quote character.

3. Start by converting this csv file in a dictionary:
```python csv_to_dict.py CameraReadyPapers.csv crdict.pickle```

4. Then process the papers using
```python process_folders.py crdict.pickle CameraReadyPapers papers suppmat vXpermissions```
The main papers will go under `papers/`
The supplementary materials under `suppmat/`
The publication agreements under `xVpermissions/`

## Steps to follow to use the paper checker locally
* you might need to install pyPdf (`pip install pyPdf` should work)
* you might need to run the script directly in the folder containing the pdf
* you might need to install a recent `netbpm` to be able to run `pamflip`. (The Debian/Ubuntu version does not contain pamflip.) The super stable version from sourceforge is fine https://sourceforge.net/projects/netpbm/files/
You might need to install `libsvga1` and `libtiff4-dev`
To do so on Ubuntu, you may need to add deb http://cz.archive.ubuntu.com/ubuntu precise main universe to your /etc/apt/sources.list

Check styles for all files with
```cd papers
cp ../checkAISTATSpaper.py .
for filename in *.pdf ; do echo $filename; python checkAISTATSpaper.py $filename ; done | tee -a log_checker```

This will save your output to `log_checker` while also displaying it to screen.

Process the output of this file:
```
cd ..
python process_log_checker.py papers/log_checker papers papers_ok papers_notok crdict.pickle```
