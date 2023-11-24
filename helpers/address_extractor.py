from natasha import AddrExtractor, MorphVocab


class AddresExtractor:
    def __init__(self):
        morph_vocab = MorphVocab()
        self.natasha_extractor = AddrExtractor(morph=morph_vocab)

        
    def get_address(self, text):
        natasha_res = self.natasha_extractor.find(text)
        return " ".join([i.type + " " + i.value for i in natasha_res.fact.parts])