#!/usr/bin/env python

text = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="folia.xsl"?>
<FoLiA xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://ilk.uvt.nl/folia" xml:id="untitleddoc" generator="libfolia-v2.5" version="2.2.1">
  <metadata type="native">
    <annotations>
      <token-annotation alias="tokconfig-nld" set="https://raw.githubusercontent.com/LanguageMachines/uctodata/master/setdefinitions/tokconfig-nld.foliaset.ttl">
        <annotator processor="ucto.1"/>
      </token-annotation>
      <paragraph-annotation>
        <annotator processor="ucto.1"/>
      </paragraph-annotation>
      <sentence-annotation>
        <annotator processor="ucto.1"/>
      </sentence-annotation>
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
      <s xml:id="untitleddoc.p.1.s.1">
        <t>Hello world.</t>
        <w xml:id="untitleddoc.p.1.s.1.w.1" class="WORD">
          <t>Hello</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.1.w.2" class="WORD" space="no">
          <t>world</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.1.w.3" class="PUNCTUATION">
          <t>.</t>
        </w>
      </s>
      <s xml:id="untitleddoc.p.1.s.2">
        <t>This is a test.</t>
        <w xml:id="untitleddoc.p.1.s.2.w.1" class="WORD">
          <t>This</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.2.w.2" class="WORD">
          <t>is</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.2.w.3" class="WORD">
          <t>a</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.2.w.4" class="WORD" space="no">
          <t>test</t>
        </w>
        <w xml:id="untitleddoc.p.1.s.2.w.5" class="PUNCTUATION">
          <t>.</t>
        </w>
      </s>
    </p>
    <p xml:id="untitleddoc.p.2">
      <s xml:id="untitleddoc.p.2.s.1">
        <t>The capital of The Netherlands is Amsterdam.</t>
        <w xml:id="untitleddoc.p.2.s.1.w.1" class="WORD">
          <t>The</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.2" class="WORD">
          <t>capital</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.3" class="WORD">
          <t>of</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.4" class="WORD">
          <t>The</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.5" class="WORD">
          <t>Netherlands</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.6" class="WORD">
          <t>is</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.7" class="WORD" space="no">
          <t>Amsterdam</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.1.w.8" class="PUNCTUATION">
          <t>.</t>
        </w>
      </s>
      <s xml:id="untitleddoc.p.2.s.2">
        <t>The government, however, always convenes in The Hague.</t>
        <w xml:id="untitleddoc.p.2.s.2.w.1" class="WORD">
          <t>The</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.2" class="WORD" space="no">
          <t>government</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.3" class="PUNCTUATION">
          <t>,</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.4" class="WORD" space="no">
          <t>however</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.5" class="PUNCTUATION">
          <t>,</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.6" class="WORD">
          <t>always</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.7" class="WORD">
          <t>convenes</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.8" class="WORD">
          <t>in</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.9" class="WORD">
          <t>The</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.10" class="WORD" space="no">
          <t>Hague</t>
        </w>
        <w xml:id="untitleddoc.p.2.s.2.w.11" class="PUNCTUATION">
          <t>.</t>
        </w>
      </s>
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

