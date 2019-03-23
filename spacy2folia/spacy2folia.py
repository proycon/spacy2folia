import argparse
import spacy
import os
import folia.main as folia

def convert(doc: spacy.tokens.doc.Doc, document_id: str = "untitled", model = None, **kwargs) -> folia.Document:
    setprefix = kwargs.get('setprefix','https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/spacy/spacy')
    processor = folia.Processor.create(name="spacy2folia")
    subprocessor = folia.Processor(name="spacy", version=spacy.__version__)
    processor.append(subprocessor)
    if model is not None and hasattr(model,'meta'):
        datasource = folia.Processor(name=model.meta['name'] + "_" + model.meta['lang'], type=folia.ProcessorType.DATASOURCE, version = model.meta['version'])
        subprocessor.append(datasource)
        for key, value in model.meta.items():
            if key not in ('name','lang','version'): #we already covered those
                if isinstance(value, str):
                    datasource.metadata[key] = value
                elif isinstance(value, list):
                    datasource.metadata[key] = ",".join(value)
        if setprefix not in kwargs:
            setprefix += "-" + model.meta['name'].replace(" ","_") + "_" + model.meta['lang']
    elif setprefix not in kwargs:
        if doc.lang_:
            setprefix += "-" + doc.lang_
        else:
            setprefix += "-unknown"
    foliadoc = folia.Document(id=document_id, autodeclare=True, processor=processor, debug=kwargs.get('debug',0) )
    if doc.lang_:
        foliadoc.metadata['lang'] = doc.lang_
    body = foliadoc.append(folia.Text(foliadoc, id=document_id + ".text"))
    paragraphs = kwargs.get('paragraphs', False)
    newparagraph = True
    if paragraphs and newparagraph:
        paragraph = body.append(folia.Paragraph)
        anchor = paragraph
    else:
        anchor = body
    for sentence in doc.sents:
        foliasentence = anchor.append(folia.Sentence)
        foliawords = [] #will map 1-1 to the spacy tokens, may contain None elements for linebreaks
        foliaword = None
        tokens = list(sentence)
        for i, word in enumerate(tokens):
            text = word.text
            if text == "\n":
                if foliaword is not None and i < len(tokens) - 1:
                    foliasentence.append(folia.Linebreak)
                    foliaword.space = True #in case a linebreak occurs in a sentence
                elif paragraphs:
                    anchor = paragraph = body.append(folia.Paragraph)
                else:
                    body.append(folia.Whitespace)
                foliawords.append(None)
            elif text.strip():
                space = word.whitespace_ != ""
                foliaword = foliasentence.append(folia.Word, text.strip(), space=space)

                if word.tag_:
                    foliaword.append(folia.PosAnnotation, set=setprefix+"-pos", cls=word.tag_)
                if word.pos_:
                    foliaword.append(folia.PosAnnotation, set="https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/universal-pos.foliaset.ttl", cls=word.pos_)
                if word.lemma_:
                    foliaword.append(folia.LemmaAnnotation, set=setprefix+"-lemma", cls=word.lemma_)
                foliawords.append(foliaword)


        for entity in sentence.ents:
            spanwords = [ w for w in foliawords[entity.start-sentence.start:entity.end-sentence.end] if w is not None ]
            foliaentity = foliasentence.add(folia.Entity, *spanwords, set=setprefix+"-namedentitities", cls=entity.label_)

        for chunk in sentence.noun_chunks:
            spanwords = [ w for w in foliawords[chunk.start-sentence.start:chunk.end-sentence.end] if w is not None ]
            foliaentity = foliasentence.add(folia.Chunk, *spanwords, set=setprefix+"-nounchunks", cls=chunk.label_)

        for i, word in enumerate(tokens):
            if word.dep_:
                depword = foliawords[i]
                headword  = foliawords[word.head.i-sentence.start]
                dependency = foliasentence.add(folia.Dependency, set=setprefix+"-dependencies", cls=word.dep_)
                dependency.append(folia.DependencyHead, headword)
                dependency.append(folia.DependencyDependent, depword)




    if paragraphs: #ensure last paragraph isn't empty
        try:
            paragraph.text()
        except folia.NoSuchText:
            body.remove(paragraph)
    return foliadoc

def main():
    parser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m','--model', type=str,help="Spacy model to load", action='store')
    parser.add_argument('-P','--no-paragraphs',dest="noparagraphs", help="Disable paragraph inference", action='store_true')
    parser.add_argument('--stdout', help="Output to standard output instead of writing files", action='store_true')
    parser.add_argument('files', nargs='+', help="Input files (plain text)")
    args = parser.parse_args()

    nlp = spacy.load(args.model)

    for filename in args.files:
        docid = ".".join(os.path.basename(filename).split(".")[:-1])
        with open(filename,'r',encoding='utf-8') as f:
            text = f.read()
        doc = nlp(text)
        foliadoc = convert(doc, docid, nlp, paragraphs=not args.noparagraphs)
        if args.stdout:
            print(foliadoc.xmlstring())
        else:
            foliadoc.save(docid + ".folia.xml")



