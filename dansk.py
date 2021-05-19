"""
    dansk.py
    ~~~~~~~~

    This module implements a decoder that translates danish words to
    their well-known english Python equivalents. Also it registers a
    codec called "dansk" on import.

    Translations worked out in collaboration with Christoffer Moesgaard
    and Robert Jensen.
"""

import argparse
import codecs
import functools
import io
from itertools import islice
import os
import pathlib
import sys
from tokenize import tokenize, untokenize, NAME, OP, TokenInfo


__version__ = "0.1.3"


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
    "elhvis": "elif",
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

    We need this function, because the tokenizer considers `elhvis`
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
            yield TokenInfo(NAME, "elhvis", t1.start, t1.end, t1.line)
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


def finish_installation():
    """Place a .pth file in site-packages that loads dansk.py.

    site.py executes *.pth files in site-packages when Python starts.
    We need this because dansk.py has to be imported before our
    beautiful ``# coding=dansk`` programs are run, so the decoder can
    be found.
    """

    def get_site_packages_path():
        virtualenv = os.environ.get("VIRTUAL_ENV")
        if virtualenv:
            from distutils.sysconfig import get_python_lib
            return get_python_lib()
        import site
        return site.getusersitepackages()

    site_packages = pathlib.Path(get_site_packages_path())
    # prefixed with zzz, because they are executed alphabetically and
    # dansk.py has to be on path before it can be imported
    dansk_pth = site_packages / "zzz_register_dansk_encoding.pth"
    with open(dansk_pth, "w+") as f:
        f.write("import dansk")


def main():
    parser = argparse.ArgumentParser(
        prog="dansk",
        description="Python, men dansk.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "installér",
        nargs=argparse.REMAINDER,
        help="dansk.py indlæses når Python startes.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="skriv version information og stop.",
    )
    parser.add_argument(
        "-h", "--hjælp", action="help", help="vis denne besked og stop."
    )
    args = parser.parse_args()

    if len(args.installér):
        finish_installation()
    else:
        print("dansk: mangler kommando\nPrøv 'dansk --hjælp' for mere information.")
        sys.exit(0)


if __name__ == "__main__":
    main()
