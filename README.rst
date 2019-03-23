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

Results in a document ``test.folia.xml`` in the current working directory.

From Python:

.. code::

   import spacy
   from spacy2folia import spacy2folia

   text = "Input text goes here"

   nlp = spacy.load("en_core_web_sm")
   doc = nlp(text)
   foliadoc = spacy2folia.convert(doc, "example", paragraphs=True)
   folia.doc.save("/tmp/example.folia.xml")


