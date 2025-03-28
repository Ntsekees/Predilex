
# WHAT IS PREDILEX

Predilex is a thesaurus of sememes represented as predicates, each having a unique identifying ID, along with definitions in English or other languages, as well as cross-references with lemmas and lexical units in various natural and engineered languages, semantic categorization and tagging, listing of hypernyms and hyponyms, and a variety of other data.

The data is in the public domain and can be browsed using the [Predilex viewer](<https://ntsekees.github.io/Predilex/viewer/index.html>) interface.

## Structure of the data

The structure of the Predilex data (purpose of each field and explanation of notations) is explained [**there**](./FORMAT.md).

## Editing Predilex
The data is stored in CSV format in the file `predilex.csv`; for a better visual experience in opening the CSV file, you may want to copy its content into the Data tab of the `predilex-template.ods` template file, which is preformatted for this purpose (with adapted column sizes and color schemes). Don't overwrite this ODS file though; for editing it, the best way is to immediately save back into the CSV file, so that you don't mistakenly overwrite the template file upon saving your changes later on.

The quickest way to load the content of `predilex.csv` into `predilex-template.ods` is to do as follow:  
1. Copy the content of the CSV into the clipboard (either using a text file viewer program, or on a Linux shell, you can do this automatically with the command `cat predilex.csv | xsel -ib`).  
2. Open `predilex-template.ods` on the Data tab.  
3. Select the first empty row, then paste the content of the clipboard as unformatted text, ensuring that the correct CSV separator is selected. Discard the two header rows (containing column names) from the content of the CSV being pasted (or delete them after pasting, if need be).

If the sheet already has content in it (e.g. you already pasted Predilex data into it previously), you should first delete its content, because otherwise remnants of the previous data could remain in the cells that were empty in the normal imported data.

# License

See the file [`LICENSE.md`](LICENSE.md).

∎
