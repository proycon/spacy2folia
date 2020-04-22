Spacy-to-FoliA
===================

.. image:: https://travis-ci.com/proycon/foliapy.svg?branch=master
    :target: https://travis-ci.com/proycon/spacy2folia

.. image:: http://applejack.science.ru.nl/lamabadge.php/spacy2folia
   :target: http://applejack.science.ru.nl/languagemachines/

Convert Spacy output to `FoLiA XML <https://proycon.github.io/folia>`_ Documents.

Installation
--------------

``$ pip install spacy2folia``

Usage Example
----------------

Using the command line tool on an input file named ``test.txt``:

``$ spacy2folia --model en_core_web_sm test.txt``

This results in a document ``test.folia.xml`` in the current working directory.

You can also invoke the command line tool on one or more FoLiA documents as input:

``$ spacy2folia --model en_core_web_sm document.folia.xml``

The output file will be written to the currrent working directory (so it may overwirte the input if it's in the same
directory!)

Usage from Python:

.. code:: python

   import spacy
   from spacy2folia import spacy2folia

   text = "Input text goes here"

   nlp = spacy.load("en_core_web_sm")
   doc = nlp(text)
   foliadoc = spacy2folia.convert(doc, "example", paragraphs=True)
   foliadoc.save("/tmp/output.folia.xml")

Usage from Python with FoLiA input:

.. code:: python

   import spacy
   import folia.main as folia
   from spacy2folia import spacy2folia

   foliadoc = folia.Document(file="/tmp/input.folia.xml")
   nlp = spacy.load("en_core_web_sm")
   spacy2folia.convert_folia(foliadoc, nlp)
   foliadoc.save("/tmp/output.folia.xml")


