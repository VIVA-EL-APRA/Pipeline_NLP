import spacy

MODEL_NAME = "es_core_news_lg"
DEFAULT_TEXT = (
    "Netflix ha encontrado en el juego del calamar su nuevo fenómeno mundial. "
    "Ni siquiera en la propia plataforma contaban con ello como seguro que "
    "tampoco esperaban recibir multitud de quejas por una escena del cuarto "
    "episodio. Sin embargo han estado rápidos para responder a la indignación "
    "del público y ha introducido un cambio en el equipo."
)


def _to_eagles(token, pos_override=None):
    pos = pos_override or token.pos_
    m = token.morph

    if pos == "PROPN":
        return "NP00SP0"

    if pos == "ADP":
        return "SP"

    if pos in ("CCONJ", "CONJ"):
        return "CC"

    if pos == "SCONJ":
        return "CS"

    if pos == "ADV":
        return "RG"

    if pos == "INTJ":
        return "I"

    if pos == "PUNCT":
        ptype = m.get("PunctType", [""])[0]
        return {"Peri": "Fp", "Quot": "Fe", "Ques": "Fit", "Excl": "Fat"}.get(ptype, "Fx")

    if pos == "NOUN":
        g = _gender(m) or "C"
        n = _number(m) or "S"
        return f"NC{g}{n}000"

    if pos == "ADJ":
        g = _gender(m) or "C"
        n = _number(m) or "S"
        return f"AQ0{g}{n}00"

    if pos == "NUM":
        return "Z"

    if pos == "DET":
        ptype = m.get("PronType", [""])[0]
        if m.get("Poss", [""])[0] == "Yes" or ptype == "Prs":
            n = _number(m) or "S"
            p = _person(m) or "3"
            g = _gender(m) or "C"
            return f"DP{p}{g}{n}N"
        if ptype == "Art":
            g = _gender(m) or "C"
            n = _number(m) or "S"
            defin = m.get("Definite", [""])[0]
            if defin == "Ind":
                return f"DI0{g}{n}0"
            return f"DA0{g}{n}0"
        if ptype in ("Ind", "Indef"):
            g = _gender(m) or "C"
            n = _number(m) or "S"
            return f"DI0{g}{n}0"
        if ptype == "Dem":
            g = _gender(m) or "C"
            n = _number(m) or "S"
            return f"DD0{g}{n}0"
        g = _gender(m) or "C"
        n = _number(m) or "S"
        return f"DZ0{g}{n}0"

    if pos == "PRON":
        n = _number(m) or "S"
        ptype = m.get("PronType", [""])[0]
        p = _person(m) or "0"
        g = _gender(m) or "C"
        if ptype == "Prs":
            return f"PP{p}{g}{n}N"
        if ptype == "Dem":
            return f"PD00{n}00"
        if ptype == "Ind":
            return f"PI00{n}00"
        if ptype in ("Int", "Que"):
            return f"PT00{n}00"
        if ptype == "Rel":
            return f"PR00{n}00"
        return f"PZ0{n}00"

    if pos in ("AUX", "VERB"):
        vform = m.get("VerbForm", [""])[0]
        if vform == "Part":
            g = _gender(m) or "M"
            n = _number(m) or "S"
            return f"VMP00{n}{g}"
        if vform == "Inf":
            return "VMN0000"
        if vform == "Ger":
            return "VMG0000"
        mood = m.get("Mood", [""])[0]
        tense = m.get("Tense", [""])[0]
        mod = _mood_map(mood)
        ten = _tense_map(tense)
        p = _person(m) or "0"
        n = _number(m) or "0"
        prefix = "VA" if pos == "AUX" else "VM"
        return f"{prefix}{mod}{ten}{p}{n}0"

    return token.tag_ if token.tag_ else pos


def _mood_map(mood):
    return {"Ind": "I", "Sub": "S", "Imp": "M", "Cnd": "C"}.get(mood, "I")


def _tense_map(tense):
    return {"Pres": "P", "Past": "S", "Imp": "I", "Fut": "F", "Pqp": "L"}.get(tense, "P")


def _gender(m):
    g = m.get("Gender", [""])[0]
    if not g:
        return ""
    return {"Masc": "M", "Fem": "F", "Neut": "N", "Com": "C"}.get(g, g[0].upper())


def _number(m):
    n = m.get("Number", [""])[0]
    if not n:
        return ""
    return {"Sing": "S", "Plur": "P", "Dual": "D"}.get(n, n[0].upper())


def _person(m):
    p = m.get("Person", [""])[0]
    return p if p else ""


class NLPipeline:
    def __init__(self):
        try:
            self.nlp = spacy.load(MODEL_NAME)
        except OSError as e:
            try:
                self.nlp = spacy.load("es_core_news_sm")
            except OSError:
                raise RuntimeError(
                    f"Modelo '{MODEL_NAME}' no encontrado. "
                    f"Ejecuta: python -m spacy download {MODEL_NAME}"
                ) from e

    def procesar(self, texto):
        doc = self.nlp(texto)
        correcciones = self._corregir(doc)
        return {
            "texto_bruto": texto,
            "frases": self._segmentar(doc),
            "tokens": self._tokenizar(doc),
            "lemas": self._lematizar(doc, correcciones),
            "pos": self._pos_tagging(doc, correcciones),
            "sin_stopwords": self._quitar_stopwords(doc, correcciones),
        }

    def _corregir(self, doc):
        tokens = [t for t in doc if not t.is_space]
        correcciones = {}

        for i, token in enumerate(tokens):
            info = {}
            text = token.text.lower()
            prev_text = tokens[i - 1].text.lower() if i > 0 else ""

            if text == "siquiera":
                info["pos"] = "ADV"
                info["eagles"] = "RG"
                info["is_stop"] = True

            elif text == "embargo" and prev_text == "sin":
                info["pos"] = "CCONJ"
                info["eagles"] = "CC"
                info["is_stop"] = True

            elif text == "calamar":
                if i > 0:
                    pt = tokens[i - 1]
                    if pt.pos_ in ("DET", "ADP", "NOUN") and pt.text.lower() in (
                        "el", "del", "un", "una", "los", "las", "al"
                    ):
                        info["pos"] = "NOUN"
                        info["eagles"] = "NCMS000"

            if info:
                correcciones[token.i] = info

        return correcciones

    def _segmentar(self, doc):
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    def _tokenizar(self, doc):
        return [token.text for token in doc if not token.is_space]

    def _lematizar(self, doc, correcciones):
        return [
            {"token": token.text, "lemma": self._lemma_normalizado(token, correcciones.get(token.i, {}))}
            for token in doc
            if not token.is_space
        ]

    def _pos_tagging(self, doc, correcciones):
        return [
            {
                "token": token.text,
                "pos": self._pos_corregido(token, correcciones.get(token.i, {})),
                "tag": token.tag_,
                "eagles": self._eagles_corregido(token, correcciones.get(token.i, {})),
                "explicacion": spacy.explain(self._pos_corregido(token, correcciones.get(token.i, {}))),
            }
            for token in doc
            if not token.is_space
        ]

    def _quitar_stopwords(self, doc, correcciones):
        return [
            {
                "token": token.text,
                "lemma": self._lemma_normalizado(token, correcciones.get(token.i, {})),
                "pos": self._pos_corregido(token, correcciones.get(token.i, {})),
                "eagles": self._eagles_corregido(token, correcciones.get(token.i, {})),
            }
            for token in doc
            if not token.is_space
            and not token.is_punct
            and not self._es_stopword(token, correcciones.get(token.i, {}))
        ]

    def _pos_corregido(self, token, corr):
        return corr.get("pos", token.pos_)

    def _eagles_corregido(self, token, corr):
        if "eagles" in corr:
            return corr["eagles"]
        pos = corr.get("pos", token.pos_)
        return _to_eagles(token, pos)

    def _es_stopword(self, token, corr):
        if "is_stop" in corr:
            return corr["is_stop"]
        return token.is_stop

    def _lemma_normalizado(self, token, corr):
        if "lemma" in corr:
            return corr["lemma"]
        lemma = token.lemma_
        pos = self._pos_corregido(token, corr)
        if pos == "ADJ":
            g = token.morph.get("Gender", [""])[0]
            if g == "Fem":
                if lemma.endswith("as"):
                    lemma = lemma[:-2] + "o"
                elif lemma.endswith("a"):
                    lemma = lemma[:-1] + "o"
        return lemma
