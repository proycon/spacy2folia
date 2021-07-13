import sys
import argparse
import spacy
import os
import folia.main as folia
from spacy2folia import VERSION

SETPREFIX = 'https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/spacy/spacy'

def get_processor(model, spacydoc, setprefix):
    """Get FoLiA processors given the provided spacy model (for provenance)"""
    processor = folia.Processor.create(name="spacy2folia",version=VERSION)
    subprocessor = folia.Processor(name="spacy", version=spacy.__version__)
    processor.append(subprocessor)
    if model is not None and hasattr(model,'meta'):
        datasource = folia.Processor(name=model.meta['lang'] + "_" + model.meta['name'], type=folia.ProcessorType.DATASOURCE, version = model.meta['version'])
        subprocessor.append(datasource)
        for key, value in model.meta.items():
            if key not in ('name','lang','version'): #we already covered those
                if isinstance(value, str):
                    datasource.metadata[key] = value
                elif isinstance(value, (list,tuple)) and all( isinstance(x,str) for x in value):
                    datasource.metadata[key] = ",".join(value)
        setprefix += "-" + model.meta['lang'] + "_" + model.meta['name'].replace(" ","_")
    else:
        if spacydoc is not None and spacydoc.lang_:
            setprefix += "-" + spacydoc.lang_
        else:
            setprefix += "-unknown"
    return processor

def convert(doc: spacy.tokens.doc.Doc, document_id: str = "untitled", model = None, **kwargs) -> folia.Document:
    """Convert a spacy document to a FoLiA document"""
    setprefix = kwargs.get('setprefix',SETPREFIX)
    processor = get_processor(model, doc, setprefix)
    foliadoc = folia.Document(id=document_id, autodeclare=True, processor=processor, debug=kwargs.get('debug',0) )
    if doc.lang_:
        foliadoc.metadata['lang'] = doc.lang_
    body = foliadoc.append(folia.Text(foliadoc, id=document_id + ".text"))
    do_paragraphs = kwargs.get('paragraphs', False)
    newparagraph = True
    if do_paragraphs and newparagraph:
        paragraph = body.append(folia.Paragraph)
        anchor = paragraph
    else:
        anchor = body

    for sentence in doc.sents:
        anchor = process_sentence(foliadoc, sentence, anchor, None, setprefix, do_paragraphs)

    if do_paragraphs: #ensure last paragraph isn't empty
        try:
            anchor.text()
        except folia.NoSuchText:
            body.remove(anchor)
    return foliadoc

def process_token(word, foliaword, setprefix):
    """Process a spacy token and a foliaword, adding inline annotations"""
    if word.tag_:
        foliaword.append(folia.PosAnnotation, set=setprefix+"-pos", cls=word.tag_)
    if word.pos_:
        foliaword.append(folia.PosAnnotation, set="https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/universal-pos.foliaset.ttl", cls=word.pos_)
    if word.lemma_:
        foliaword.append(folia.LemmaAnnotation, set=setprefix+"-lemma", cls=word.lemma_)

def process_sentence(foliadoc, sentence, anchor, foliasentence, setprefix, do_paragraphs, pretokenized=False):
    """Process a spacy doc or sentence in a folia context"""
    if foliasentence is None and anchor is not None:
        foliasentence = anchor.append(folia.Sentence)
    body = foliadoc.data[0]
    assert isinstance(body, (folia.Text, folia.Speech))
    if not pretokenized:
        foliawords = [] #will map 1-1 to the spacy tokens, may contain None elements for linebreaks
        foliaword = None
        tokens = list(sentence)
        for i, word in enumerate(tokens):
            text = word.text
            if text == "\n":
                if foliaword is not None and i < len(tokens) - 1:
                    foliasentence.append(folia.Linebreak)
                    foliaword.space = True #in case a linebreak occurs in a sentence
                elif do_paragraphs:
                    anchor = body.append(folia.Paragraph)
                else:
                    body.append(folia.Whitespace)
                foliawords.append(None)
            elif text.strip():
                space = word.whitespace_ != ""
                foliaword = foliasentence.append(folia.Word, text.strip(), space=space)
                process_token(word, foliaword, setprefix)
                foliawords.append(foliaword)
    else: #pretokenized
        foliawords = list(foliasentence.words())
        tokens = list(sentence)
        for word, foliaword in zip(tokens, foliawords):
            process_token(word, foliaword, setprefix)

    if isinstance(sentence, spacy.tokens.doc.Doc):
        start = 0
        end = len(sentence)
    else:
        start = sentence.start
        end = sentence.end

    for entity in sentence.ents:
        spanwords = [ w for w in foliawords[entity.start-start:entity.end-end] if w is not None ]
        foliaentity = foliasentence.add(folia.Entity, *spanwords, set=setprefix+"-namedentitities", cls=entity.label_)

    try:
        for chunk in sentence.noun_chunks:
            spanwords = [ w for w in foliawords[chunk.start-start:chunk.end-end] if w is not None ]
            foliaentity = foliasentence.add(folia.Chunk, *spanwords, set=setprefix+"-nounchunks", cls=chunk.label_)
    except NotImplementedError as e:
        print("WARNING: Not processing noun chunks: " + str(e) ,file=sys.stderr)

    for i, word in enumerate(tokens):
        if word.dep_:
            depword = foliawords[i]
            headword  = foliawords[word.head.i-start]
            dependency = foliasentence.add(folia.Dependency, set=setprefix+"-dependencies", cls=word.dep_)
            dependency.append(folia.DependencyHead, headword)
            dependency.append(folia.DependencyDependent, depword)

    return anchor


def convert_folia(foliadoc: folia.Document, model, default_tokenizer=None, **kwargs) -> folia.Document:
    """Process an existing folia document with spacy"""
    if default_tokenizer is not None:
        model.tokenizer = default_tokenizer
    if not foliadoc.processor or foliadoc.processor.name != "spacy2folia":
        foliadoc.processor = get_processor(model, None, kwargs.get('setprefix',SETPREFIX))
    pretokenized = False
    if foliadoc.declared(folia.Sentence):
        print("Sentence annotation is present in " + foliadoc.id + ", annotating on the sentence level",file=sys.stderr)
        if foliadoc.declared(folia.Word):
            print("Token annotation is already present in " + foliadoc.id + ", disabling SpaCy's tokeniser and working on the existing tokens!",file=sys.stderr)
            model.tokenizer = WhitespaceTokenizer(model.vocab)
            pretokenized = True

        for sentence in foliadoc.sentences():
            text = sentence.text(retaintokenisation=pretokenized).replace("\n"," ").strip()
            doc = model(text)
            process_sentence(foliadoc, doc, None, sentence, kwargs.get('setprefix',SETPREFIX), do_paragraphs=False, pretokenized=pretokenized)

    elif foliadoc.declared(folia.Paragraph):
        print("Paragraph annotation is present in " + foliadoc.id + ", annotating on the paragraph level",file=sys.stderr)

        for paragraph in foliadoc.paragraphs():
            text = paragraph.text().replace("\n"," ").strip()
            doc = model(text)
            for sentence in doc.sents:
                process_sentence(foliadoc, sentence, paragraph, None, kwargs.get('setprefix',SETPREFIX), do_paragraphs=False, pretokenized=pretokenized)

    else:
        print("Nothing to do for document " + foliadoc.id + "? Couldn't find any existing structural basis to annotate.",file=sys.stderr)

    return foliadoc

class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self,text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return spacy.tokens.doc.Doc(self.vocab, words=words, spaces=spaces)


def main():
    parser = argparse.ArgumentParser(description="Run a spaCy pipeline and convert the output to FoLiA", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m','--model', type=str,help="spaCy model to load (you can enter an iso-639-1 language code such as en, de, nl, fr here)", action='store',default='en')
    parser.add_argument('-P','--no-paragraphs',dest="noparagraphs", help="Disable paragraph inference", action='store_true')
    parser.add_argument('--stdout', help="Output to standard output instead of writing files", action='store_true')
    parser.add_argument('--debug', help="Enable debug mode", action='store_true')
    parser.add_argument('--setprefix', type=str,help="The prefix for the FoLiA Set Definitions", default=SETPREFIX, action='store')
    parser.add_argument('files', nargs='+', help="Input files, either plain text or FoLiA XML (detected through extension xml)")
    args = parser.parse_args()

    nlp = spacy.load(args.model)
    default_tokenizer = nlp.tokenizer

    for filename in args.files:

        if filename.lower().endswith(".xml"):
            #FoLiA
            foliadoc = folia.Document(file=filename, autodeclare=True, processor=get_processor(nlp, None, args.setprefix), debug=args.debug )
            foliadoc = convert_folia(foliadoc, nlp, default_tokenizer)
            if args.stdout:
                print(foliadoc.xmlstring())
            else:
                foliadoc.save(os.path.basename(foliadoc.filename))
        else:
            docid = ".".join(os.path.basename(filename).replace(" ","_").split(".")[:-1])
            if not folia.isncname(docid):
                if docid[0].isnumeric():
                    docid = "D" + docid
                docid = docid.replace(":","_").replace(" ","_")
            #plain text
            with open(filename,'r',encoding='utf-8') as f:
                text = f.read()
            doc = nlp(text)
            foliadoc = convert(doc, docid, nlp, paragraphs=not args.noparagraphs)
            if args.stdout:
                print(foliadoc.xmlstring())
            else:
                foliadoc.save(docid + ".folia.xml")



