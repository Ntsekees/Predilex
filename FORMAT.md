
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

An indicative estimation of the potential of the predicate's word to be used as an etymological component in compound words.

## arity

The arity (or ‘valency’, or ‘adicity’) of the predicate, i.e. the number of argument slots it has (excluding the hidden context variable slot).

## types

A list of letters or digits separated by whitespaces, each sign representing the type of the corresponding argument slot of the predicate, in the same order of appearance as in the predicate's definition.

## distributivity

A list of letters separated by whitespaces; each letter corresponds to one of the predicate's argument slots, and each letter indicates its behavior with respect to distributivity: `d` for “distributive”, `c` for “collective”, `s` for exclusively singular references. When a property P is distributive, this means that `P(x)` entails `∀y. among(y, x) ⇒ P(y)`.

## kind handling

This column is deprecated. It was intended to indicates the behavior of each argument slot with respect to Kind handling, between the following options: `s` for “stage-level”, `i` for “individual-level”, and `k` for “kind-level”.

## slot tags
Lists of semantic categorization tags separated by whitespaces, in groups separated by semicolons `;`, each group being associated with one of the slots of the predicate, in order.

Each group indicates the semantic categories associated with the targed argument slot.

## tags

A single list of semantic categorization tags separated by whitespaces, describing the predicate as a whole, and not one of its argument slots in particular.

## possible etymologies

Indicative list of cherry-picked potential etymologies for words representing this predicate. The potential etymologies are separated by semicolons `;`. Each potential etymology consists of a list of Predilex ID's, separated by whitespaces.

## homoeventives

List of Predilex ID's separated by whitespaces. Each such ID represents a predicate which describes the same event as the current predicate, but typically with a different argument structure, as exemplified by the following pair:
* 𝜆x. eats(x)
* 𝜆x. 𝜆y. eats(x, y)

## similar

List of Predilex ID's separated by whitespaces. Each such ID represents a predicate whose meaning is similar to that of that of the current predicate, i.e. a quasi-synonym thereof.

## antonyms

Same format as the above, but listing antonyms for the predicate.

## hypernyms

Same format as the above, but listing hypernyms for the predicate.

## hyponyms

Same format as the above, but listing hyponyms for the predicate.

## holonyms

Same format as the above, but listing holonyms for the predicate.

## meronyms

Same format as the above, but listing meronyms for the predicate.

## related

Same format as the above, but listing related predicates, as a sort of ‘see also’.

## alt

Same format as the above, but listing predicates that can function as alternatives to the current predicate, usually with a homologuous meaning but a different argument structure. Typically, a single language would need only one of the alternatives, and having several of them at once would be redundant.

Some prominent examples may be the following pairs:  
* ⟪➊ is a hand⟫ versus ⟪➊ is a hand part of ➋⟫;
* ⟪➊ surpasses ➋ in the amount to which they satisfy the gradable property ➌⟫ versus ⟪➊ surpasses ➋ in the amount they are in relation ➌ with⟫.

## definition

Formal, substitutional definition of the predicate, written in a custom logic notation, with argument slots expressed as lambda expressions. Predilex ID's are used as predicate identifiers in the logic notation, allowing defining the current predicate in terms of other predicates in the Predilex dataset.

## positive sample media

A list of URLs separated by vertical pipes `|` surrounded by one whitespace on each side. Each URL points to a media, such as an image or a sound file, representing an instance of the predicate, a physical realization thereof. Such media may serve for example for teaching the meaning of the predicate.

## negative sample media

Same as the previous field, but this time with negative sample media: select medias that do not represent instances of the predicate, whereas it might have been expected that they could have been instances thereof.
For example, when dealing with a predicate describing a pigeon, positive media like pictures of pigeons might still allow for the supposition that the predicate could have a broader meaning, allowing for other sorts of birds to quality; by adding non-pigeon birds as negative sample media, the boundaries of application of the predicate are made clearer.

## symbols

Glyphs, symbols, pictograms or ideograms representing the predicate at hand.


