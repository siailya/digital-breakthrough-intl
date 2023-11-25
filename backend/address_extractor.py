from natasha import AddrExtractor, MorphVocab


class AddressExtractor:
    def __init__(self):
        morph_vocab = MorphVocab()
        self.natasha_extractor = AddrExtractor(morph=morph_vocab)

    def get_address(self, text):
        natasha_res = self.natasha_extractor.find(text)
        if not natasha_res or not natasha_res.fact or not natasha_res.fact.parts or len(natasha_res.fact.parts) == 0:
            return ""
        return " ".join([(i.type + " " + i.value) if i.type and i.value else "" for i in natasha_res.fact.parts])


if __name__ == "__main__":
    ae = AddressExtractor()
    print(ae.get_address("Вобще парк надо чистить. Там бурелом сплошной."))