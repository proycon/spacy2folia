#!/usr/bin/env python

text = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="folia.xsl"?>
<FoLiA xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://ilk.uvt.nl/folia" xml:id="untitleddoc" generator="libfolia-v2.5" version="2.2.1">
  <metadata type="native">
    <annotations>
      <paragraph-annotation>
        <annotator processor="ucto.1"/>
      </paragraph-annotation>
      <text-annotation set="https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/text.foliaset.ttl"/>
    </annotations>
    <provenance>
      <processor xml:id="ucto.1" begindatetime="2020-04-22T18:20:17" command="ucto -Lnld test.txt text.xml" folia_version="2.2.1" host="mhysa.anaproy.nl" name="ucto" user="proycon" version="0.22">
        <processor xml:id="ucto.1.generator" folia_version="2.2.1" name="libfolia" type="generator" version="2.5"/>
        <processor xml:id="uctodata.1" name="uctodata" type="datasource" version="0.8">
          <processor xml:id="uctodata.1.1" name="tokconfig-nld" type="datasource" version="0.2"/>
        </processor>
      </processor>
    </provenance>
    <meta id="language">nld</meta>
  </metadata>
  <text xml:id="untitleddoc.text">
    <p xml:id="untitleddoc.p.1">
      <t>Hello world. This is a test.</t>
    </p>
    <p xml:id="untitleddoc.p.2">
      <t>The capital of The Netherlands is Amsterdam. The government, however, always convenes in The Hague.</t>
    </p>
  </text>
</FoLiA>
"""

import spacy
import folia.main as folia
from spacy2folia import spacy2folia

nlp = spacy.load("en_core_web_sm")
foliadoc = folia.Document(string=text)
foliadoc = spacy2folia.convert_folia(foliadoc, nlp)
print(foliadoc.xmlstring())

