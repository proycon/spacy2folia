import argparse
import spacy
import os
import folia.main as folia

def convert(doc: spacy.tokens.doc.Doc, document_id: str = "untitled", **kwargs) -> folia.Document:
    processor = folia.Processor.create(name="spacy2folia")
    foliadoc = folia.Document(id=document_id, autodeclare=True, processor=processor, debug=kwargs.get('debug',0) )
    body = foliadoc.append(folia.Text(foliadoc, id=document_id + ".text"))
    paragraphs = kwargs.get('paragraphs', False)
    setprefix = kwargs.get('setprefix','spacy')
    newparagraph = True
    if paragraphs and newparagraph:
        paragraph = body.append(folia.Paragraph)
        anchor = paragraph
    else:
        anchor = body
    for sentence in doc.sents:
        foliasentence = anchor.append(folia.Sentence)
        for word in sentence:
            text = word.text
            if text == "\n":
                if paragraphs:
                    anchor = paragraph = body.append(folia.Paragraph)
                else:
                    body.append(folia.Whitespace)
            elif text.strip():
                space = word.whitespace_ != ""
                foliaword = foliasentence.append(folia.Word, text.strip(), space=space)

                if word.tag_:
                    foliaword.append(folia.PosAnnotation, set=setprefix+"-pos-" + word.lang_, cls=word.tag_)
                if word.lemma_:
                    foliaword.append(folia.LemmaAnnotation, set=setprefix+"-lemma-" + word.lang_, cls=word.lemma_)

        words = list(foliasentence.words())

        for entity in sentence.ents:
            spanwords = words[entity.start-sentence.start:entity.end-sentence.end]
            foliaentity = foliasentence.add(folia.Entity, *spanwords, set=setprefix+"-namedentitities-" + doc.lang_, cls=entity.label_)

        for chunk in sentence.noun_chunks:
            spanwords = words[chunk.start-sentence.start:chunk.end-sentence.end]
            foliaentity = foliasentence.add(folia.Chunk, *spanwords, set=setprefix+"-nounchunks-" + doc.lang_, cls=chunk.label_)



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
        with open(filename,'r','utf-8') as f:
            text = f.read()
        doc = nlp(text)
        foliadoc = convert(doc, docid, paragraphs=not args.noparagraphs)
        if args.stdout:
            print(foliadoc.xmlstring())
        else:
            foliadoc.save(docid + ".folia.xml")



