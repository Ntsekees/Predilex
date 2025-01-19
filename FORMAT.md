
# FORMAT

The Predilex data presents itself in the form of a grid with many named columns, and rows each representing a different entry, dedicated to one semantic predicate, or ‘sememe’.

The two first rows constitute the header, giving out the names of each column: on the first row (hidden in the ODS template file) is a shortened code name, and on the second row a longer, ‘full’ name for the column.

Below is an explanation of the purpose of each column, in order:

## id

The Predilex ID of the entry. It uniquely identify the predicate in Predilex, and is also used in other columns of other entries for referring back to the current entry (for example, for indicating that the other entry's predicate is a hyponym of the one of the entry at hand).

A Predilex ID has the shape `CVCVCV` where `C` represents one of 20 consonant letters (`bcdfghjklmnpqrstvwyz`), and `V` one of 5 vowel letters (`aeiou`), making for 100 possible `CV` syllables, and 1000000 possible `CVCVCV` ID's.

## rank

The Rank is a single lowercase letter that gives an estimation of the use frequency of the predicate in real language use.

## compoundability

## arity

The arity (or ‘valency’, or ‘adicity’) of the predicate, i.e. the number of argument slots it has (excluding the hidden context variable slot).

## types
A list of letters or digits separated by whitespaces, each sign representing the type of the corresponding argument slot of the predicate, in the same order of appearance as in the predicate's definition.

## distributivity

## kind handling

## slot tags

## tags

The tags list what category a given predicate belongs to. For example: mathematics, modality, biology.

## possible etymologies

