# Converting Latin Prose to Poetry

The Latin language has two features that make its poetry distinct:

* First, Latin has formal rules for determining whether a syllable is long or short, and Latin poetry always follows specific patterns, or meters, of long and short syllables.  

* Second, Latin encodes most of the information that English conveys through word position into the words themselves.  This means that it is often possible to rearrange the order of words a Latin sentence completely without changing the meaning.

Together, these facts mean that it is sometimes possible to turn Latin prose into poetry simply by rearranging the words in each sentence to fit a meter.  This simple "metrifier" is limited in scope, but it serves as an effective proof-of-concept that this can be done algorithmically.

## Software Requirements

### Language

Python 3

### Libraries

NLTK, CLTK

This metrifier uses the [Natural Language Toolkit](https://www.nltk.org/) and the [Classical Languages Toolkit](http://cltk.org/).  Both libraries can be installed using pip.

This repository also uses a modified copy of CLTK's scanner as a workaround for an issue with the original code.

### Convenient Macronizer

[Johan Winge's macronizer](http://stp.lingfil.uu.se/~winge/macronizer/index.py) is highly recommended for users who do not wish to macronize (mark naturally-long syllables) their input by hand.

## Running the Code

To run the code, run main.py and follow the command-line prompts that appear.

By default, the program is set to use the included corpus "hendecasyllabics.txt", 530 lines of machine-macronized hendecasyllabic meter from Catullus, whenever a corpus is required.  However, you may enter an alternative text file if you prefe with each line of hendecasyllabic meter on its own line in the text file.

All of the code's functions expect macronized input, and will attempt to match it to hendecasyllabic meter.