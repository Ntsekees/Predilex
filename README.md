
# WHAT IS PREDILEX

Predilex is a database of predicates, with definitions in English or other languages, along with cross-referencing with lexical units from several logical languages, semantic categorization and tagging, listing of hypernyms and hyponyms, and a variety of other data.

The data is stored in CSV format in the file `predilex.csv`; for a better visual experience, you may want to copy its content into the Data tab of the `predilex-template.ods` file, which is preformatted for this purpose (with adapted column sizes and color schemes). Don't overwrite this ODS file though; you should instead save it to another file (e.g. `predilex.ods`) which won't be tracked by Git, so that you don't need to import from the CSV file every time you want to see the data in the preformatted sheet. If you do that though, please be careful of always saving your changes to the CSV file before pulling changes made by other people in the remote repository, and then import them back to your ODS file, lest you take the risk of overwriting other people's work by mistake later on!

## Viewing/Editing Predilex
The quickest way to load the content of `predilex.csv` into `predilex-template.ods` is to do as follow:  
1. Copy the content of the CSV into the clipboard (either using a text file viewer program, or on a Linux shell, you can do this automatically with the command `cat predilex.csv | xsel -ib`).  
2. Open `predilex-template.ods` on the Data tab.  
3. Select the first empty row, then paste the content of the clipboard as unformatted text, ensuring that the correct CSV separator is selected. Discard the two header rows (containing column names) from the content of the CSV being pasted (or delete them after pasting, if need be).

If the sheet already has content in it (e.g. you already pasted Predilex data into it previously), you should first delete its content, because otherwise remnants of the previous data could remain in the cells that were empty in the normal imported data.

The Predilex data may also be viewed in readonly in Google Sheets at the following address:
https://docs.google.com/spreadsheets/d/1z_k_gHH67rBpQTgBOP6diBU-X163jowd-gWxC1CUfEI/edit?usp=sharing

# Structure

The structure of the Predilex data (purpose of each column and explanation of notations) is explained [**there**](./FORMAT.md).

# License

See the file [`LICENSE.md`](LICENSE.md).

∎
