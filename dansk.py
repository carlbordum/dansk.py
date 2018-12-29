"""
    dansk.py
    ~~~~~~~~

    This module implements a decoder that translates danish words to
    their well-known english Python equivalents. Also it registers a
    codec called "dansk" on import.

    Translations worked out in collaboration with Christoffer Moesgaard
    and Robert Jensen.
"""

import codecs
import functools
import io
from itertools import islice
from tokenize import tokenize, untokenize, NAME, OP, TokenInfo


__version__ = "0.1.2"


_viking_to_english = {
    "og": "and",
    "som": "as",
    # `hævd`, `påstå` og `postulèr` blev overvejet som
    # alternativer, men `forvent` vandt, da `ForventningsFejl` giver
    # mest mening som undtagelse.
    "forvent": "assert",
    # Valgt istedet for `asynk` med begrundelsen at den eneste grund
    # til at det ikke er `asynchronous` er at ingen kan stave til det.
    "asynkron": "async",
    "afvent": "await",
    "brud": "break",
    # Hvis `klasse` ikke var et accepteret datalogisk begreb ville vi
    # nok have valgt `slags` eller `art`.
    "klasse": "class",
    "fortsæt": "continue",
    "lad": "def",
    "slet": "del",
    "ellers-hvis": "elif",
    "ellers": "else",
    "pånær": "except",
    "slutteligt": "finally",
    "for-hver": "for",
    "fra": "from",
    "altomfattende": "global",
    "hvis": "if",
    "indfør": "import",
    "indeni": "in",  # we don't want to disallow `i` as a variable name
    "er": "is",
    "λ": "lambda",
    "omfattende": "nonlocal",
    "ikke": "not",
    "eller": "or",
    "fisk": "pass",
    "hejs": "raise",
    "aflever": "return",
    "forsøg": "try",
    "medens": "while",
    "brug": "with",
    # Den her var virkelig svær. Der var mange gode bud, men i sidste
    # ende må vi konstatere at `yd` er bedst, så længe man lytter til
    # https://youtu.be/llyedDrGQkA, mens man skriver sine generatorer.
    "yd": "yield",
    "Falsk": "False",
    "Sand": "True",
    "Intet": "None",
}


def encode(string, errors="strict"):
    # this could return the default encode, but I think
    #     encode(decode(source)) == source
    # which is not possible for this encoding

    # unless we don't allow regular python keywords at all
    # hmmmm
    raise NotImplemented()


def _token_iter(tokens):
    """Collapse tokens considered a single token in danish into one.

    We need this function, because the tokenizer considers `ellers-hvis`
    and `for-hver` as "ellers" MINUS "hvis" and "for" MINUS "hver"
    respectively.

    Send the tokenized danish code through this guy.
    """
    if len(tokens) < 3:
        yield from tokens
        return

    def _is_elif_token(t1, t2, t3):
        return (
            t1.type == NAME
            and t1.string == "ellers"
            and t2.type == OP
            and t2.string == "-"
            and t3.type == NAME
            and t3.string == "hvis"
        )

    def _is_for_token(t1, t2, t3):
        return (
            t1.type == NAME
            and t1.string == "for"
            and t2.type == OP
            and t2.string == "-"
            and t3.type == NAME
            and t3.string == "hver"
        )

    skip = 0  # skip this many tokens before proceding
    for t1, t2, t3 in zip(tokens, islice(tokens, 1, None), islice(tokens, 2, None)):
        if skip > 0:
            skip -= 1
            continue

        if _is_elif_token(t1, t2, t3):
            yield TokenInfo(NAME, "ellers-hvis", t1.start, t1.end, t1.line)
            skip = 2
        elif _is_for_token(t1, t2, t3):
            yield TokenInfo(NAME, "for-hver", t1.start, t1.end, t1.line)
            skip = 2
        else:
            yield t1

    yield tokens[-2]
    yield tokens[-1]


# pass True for ignore_first_line if the byteslike still contains the dansk
# encoding comment
def decode(byteslike, errors="replace", *, ignore_first_line):
    read_code = io.BytesIO(bytes(byteslike)).readline
    if ignore_first_line:
        read_code()  # its the encoding comment

    tokens = list(tokenize(read_code))

    new_tokens = []
    for token in _token_iter(tokens):
        if token.string in _viking_to_english:
            new_tokens.append(
                TokenInfo(
                    token.type,
                    _viking_to_english[token.string],
                    token.start,
                    token.end,
                    token.line,
                )  # its a copy with token.string replaced
            )
        else:
            new_tokens.append(token)

    return str(untokenize(new_tokens), "utf-8"), len(byteslike)


# codecs.BufferedIncrementalDecoder is undocumented, but well commented, and if
# it breaks, it's easy to copy/paste it here
class DanskIncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, data, errors, final):
        if final:
            # this thing is used when python has already removed the encoding
            # comment, so tell our decode() to not do it
            return decode(data, errors, ignore_first_line=False)
        else:
            return ("", 0)


codec_info = codecs.CodecInfo(
    encode,
    functools.partial(decode, ignore_first_line=True),
    incrementaldecoder=DanskIncrementalDecoder,
    name="dansk",
)
codecs.register({"dansk": codec_info}.get)
