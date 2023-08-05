#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Library of regular expression patterns.
"""
import re
import enum

from .tlds import tlds


class pattern:
    """
    A wrapper for regular expression pattern objects created from re.compile,
    allowing combination of several patterns into one via overloaded
    operators.
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.compiled = re.compile(bytes(self))

    def __bytes__(self):
        return str(self).encode('ascii')

    def __str__(self):
        return self.pattern

    def __getattr__(self, verb):
        return getattr(self.compiled, verb)


class alphabet(pattern):
    """
    A pattern object representing strings of letters from a given alphabet, with
    an optional prefix and postfix.
    """
    def __init__(self, repeat, prefix='', postfix='', at_least=1, at_most=None, **kwargs):
        if not at_most:
            count = '+' if at_least <= 1 else '{{{},}}'.format(at_least)
        else:
            count = '{{{},{}}}(?!{})'.format(at_least, at_most, repeat)

        pattern.__init__(self,
            R'{b}(?:{r}){c}{a}'.format(
                r=repeat,
                b=prefix,
                c=count,
                a=postfix
            ),
            **kwargs
        )


class tokenize(pattern):
    """
    A pattern representing a sequence of tokens matching the `token` pattern, separated
    by sequences matching the pattern `sep`. The optional parameter `bound` is required
    before and after each token, its default value is the regular expression zero length
    match for a word boundary.
    """
    def __init__(self, token, sep, bound='\\b', **kwargs):
        pattern.__init__(
            self,
            R'(?:{b}{t}{b}{s})+(?:{b}{t}{b})?'.format(
                s=sep, b=bound, t=token),
            **kwargs
        )


class PatternEnum(enum.Enum):
    @classmethod
    def get(cls, name, default):
        try:
            return cls[name]
        except KeyError:
            return default

    def __str__(self):
        return str(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __repr__(self):
        return F'<pattern {self.name}: {self.value}>'

    def __getattr__(self, name):
        if name in dir(re.Pattern):
            return getattr(self.value, name)
        raise AttributeError


__TLDS = R'(?i:{possible_tld})(?!(?:{dealbreakers}))'.format(
    possible_tld='|'.join(tlds),
    dealbreakers='|'.join([
        R'[a-z]',
        R'[A-Za-z]{3}',
        R'\.\w\w',
        R'\([\'"\w)]'
    ])
)

# see https://tools.ietf.org/html/rfc2181#section-11
format_domain_normal = (
    R'(?:[a-zA-Z0-9\_][a-zA-Z0-9\-\_]{{0,62}}?\.){repeat}'
    R'[a-zA-Z0-9\_][a-zA-Z0-9\-\_]{{1,62}}\.{tlds}'
)
format_domain_defang = (
    R'(?:[a-zA-Z0-9\_][a-zA-Z0-9\-\_]{{0,62}}?(?:\[\.\]|\.)){repeat}'
    R'[a-zA-Z0-9\_][a-zA-Z0-9\-\_]{{1,62}}(?:\[\.\]|\.){tlds}'
)

pattern_domain = format_domain_normal.format(repeat='{0,20}', tlds=__TLDS)

pattern_subdomain = format_domain_normal.format(repeat='{1,20}', tlds=__TLDS)
pattern_domain_df = format_domain_defang.format(repeat='{0,20}', tlds=__TLDS)

pattern_version = '|'.join('.' * k + 'version' + '.' * (10 - k) for k in range(10))

pattern_octet = R'(?:1\d\d|2[1-4]\d|25[1-5]|[1-9]?\d)'
pattern_ipv4 = R'(?<!\.|\d)(?:{o}\.){{3}}{o}(?![\d\.])'.format(o=pattern_octet)
pattern_ipv4_df = R'(?:{o}{d}){{3}}{o}'.format(o=pattern_octet, d=R'(?:\[\.\]|\.)')

pattern_socket = '(?:{ip}|{d})(?::\\d{{2,5}})'.format(ip=pattern_ipv4, d=pattern_domain)
pattern_hostname = pattern_socket + '?'
pattern_hostname_df = '(?:{ip}|{d})(?::\\d{{2,5}})?'.format(ip=pattern_ipv4_df, d=pattern_domain_df)

pattern_integer = '[-+]?(?:0[bB][01]+|0[xX][0-9a-fA-F]+|0[1-7][0-7]*|[1-9][0-9]*|0)(?![a-zA-Z0-9])'
pattern_float = R'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
pattern_cmdstr = R'''(?:"(?:""|[^"])*"|'(?:''|[^'])*')'''
pattern_ps1str = R'''(?:"(?:`.|""|[^"])*"|'(?:''|[^'])*')'''
pattern_string = R'''(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')'''

pattern_vbe = R'''#@~\^[ -~]{6}==(?:.*?)[ -~]{6}==\^#~@'''

pattern_url = ''.join([
    R'([a-zA-Z]{2,20}?://'                    # scheme
    R'(?:[^"\'\s\x00-\x20\x7E-\xFF]{1,256}?'  # username
    R'(?::[^"\'\s\x00-\x20\x7E-\xFF]{0,256}?)?@)?',
    pattern_socket + '?',
    R'(?:[/?#](?:[~/_=?&.,\w\%\-](?![a-zA-Z]{2,20}://))*)?)'
])

pattern_url_df = ''.join([
    R'([a-zA-Z]{2,20}?(?:\[:\]|:)//'          # scheme
    R'(?:[^"\'\s\x00-\x20\x7E-\xFF]{1,256}?'  # username
    R'(?::[^"\'\s\x00-\x20\x7E-\xFF]{0,256}?)?@)?',
    pattern_socket + '?',
    R'(?:[/?#](?:[/_=?&.,\w\%\-](?![a-zA-Z]{2,20}://))*)?)'
])

pattern_email = R'(?:[a-zA-Z0-9_\.\+\-]{{1,256}}?)@(?:{})'.format(pattern_domain)
pattern_guid = R'(?:\b|\{)[0-9A-Fa-f]{8}(?:\-[0-9A-Fa-f]{4}){3}\-[0-9A-Fa-f]{12}(?:\}|\b)'

pattern_pathpart_nospace = R'[-\w+,.;@\]\[\^`~]+'  # R'[^/\\:"<>|\s\x7E-\xFF\x00-\x1F\xAD]+'
pattern_win_path_element = R'(?:{n} ){{0,4}}{n}'.format(n=pattern_pathpart_nospace)
pattern_nix_path_element = R'(?:{n} ){{0,1}}{n}'.format(n=pattern_pathpart_nospace)
pattern_win_env_variable = R'%[a-zA-Z][a-zA-Z0-9_\-\(\)]{2,}%'

pattern_win_path = R'(?:{s})(?P<pathsep>[\\\/])(?:{p}(?P=pathsep))*{p}\b'.format(
    s='|'.join([
        pattern_win_env_variable,     # environment variable
        R'[A-Za-z]:',                 # drive letter with colon
        R'\\\\[a-zA-Z0-9_.$]{1,50}',  # UNC path
        R'HK[A-Z_]{1,30}',            # registry root key
    ]),
    p=pattern_win_path_element
)

pattern_nix_path = R'\b/?(?:{n}/){{2,}}{n}\b'.format(n=pattern_nix_path_element)
pattern_path = R'(?:{nix})|(?:{win})'.format(
    nix=pattern_nix_path,
    win=pattern_win_path
)

pattern_hexline = R'(?:{s}+\s+)?\s*{h}(?:\s+{s}+)?'.format(
    h=tokenize(
        R'(?:0x)?[0-9a-f]{2}h?',
        sep=R'[- \t\/:;,\\]{1,3}'
    ).pattern,
    s=R'[-\w:;,#\.\$\?!\/\\=\(\)\[\]\{\}]'
)

pattern_pem = (
    R'-----BEGIN(?:\s[A-Z0-9]+)+-----{n}'
    R'(?:{b}{{40,100}}{n})+{b}{{1,100}}={{0,3}}{n}'
    R'-----END(?:\s[A-Z0-9]+)+-----'
).format(n=R'(?:\r\n|\n\r|\n)', b=R'[0-9a-zA-Z\+\/]')

__all__ = [
    'pattern',
    'alphabet',
    'tokenize',
    'formats',
    'indicators',
    'defanged'
]


class formats(PatternEnum):
    """
    An enumeration of patterns for certain formats.
    """
    integer = pattern(pattern_integer)
    "Integer expressions"
    float = pattern(pattern_float)
    "Floating point number expressions"
    string = pattern(pattern_string)
    "C syntax string literal"
    cmdstr = pattern(pattern_cmdstr)
    "Windows command line escaped string literal"
    ps1str = pattern(pattern_ps1str)
    "PowerShell escaped string literal"
    printable = alphabet(R'[ -~]')
    "Any sequence of printable characters"
    intarray = tokenize(pattern_integer, sep=R'\s*[;,]\s*', bound='')
    "Sequences of integers, separated by commas or semicolons"
    word = alphabet(R'\\w')
    "Sequences of word characters"
    alph = alphabet(R'[a-zA-Z]')
    "Sequences of alphabetic characters"
    vbe = pattern(pattern_vbe)
    "Encoded Visual Basic Scripts"
    anum = alphabet(R'[a-zA-Z0-9]')
    "Sequences of alpha-numeric characters"
    b64 = alphabet(R'[0-9a-zA-Z\+\/]', postfix=R'[0-9a-zA-Z\+\/]{0,3}={0,3}')
    "Base64 encoded strings"
    b64u = alphabet(R'[0-9a-zA-Z\_\-]', postfix=R'[0-9a-zA-Z\_\-]{0,3}={0,3}')
    "Base64 encoded strings using URL-safe alphabet"
    hex = alphabet(R'[0-9a-fA-F]')
    "Hexadecimal strings"
    HEX = alphabet(R'[0-9A-F]')
    "Uppercase hexadecimal strings"
    hexdump = tokenize(pattern_hexline, bound='', sep=R'\s*\n')
    """
    This pattern matches a typical hexdump output where hexadecimally encoded
    bytes are followed by a string which contains dots or printable characters
    from the dump. For example:

        46 4F 4F 0A 42 41 52 0A  FOO.BAR.
        F0 0B AA BA F0 0B        ......
    """
    hexarray = tokenize(R'[0-9A-F]{2}', sep=R'\s*[;,]\s*', bound='')
    "Arrays of hexadecimal strings, separated by commas or semicolons"


class indicators(PatternEnum):
    """
    An enumeration of patterns for indicators.
    """
    domain = pattern(pattern_domain)
    "Domain names"
    email = pattern(pattern_email)
    "Email addresses"
    guid = pattern(pattern_guid)
    "Windows GUID strings"
    ipv4 = pattern(pattern_ipv4)
    "String representations of IPv4 addresses"
    md5 = alphabet('[0-9a-f]', at_least=32, at_most=32)
    "Hexadecimal strings of length 32"
    sha = alphabet('[0-9a-f]', at_least=40, at_most=40)
    "Hexadecimal strings of length 40"
    sha256 = alphabet('[0-9a-f]', at_least=64, at_most=64)
    "Hexadecimal strings of length 64"
    hostname = pattern(pattern_hostname)
    "Any domain name or IPv4 address, optionally followd by a colon and a port number."
    socket = pattern(pattern_socket)
    "Any domain name or IPv4 address followed by a colon and a (port) number"
    subdomain = pattern(pattern_subdomain)
    "A domain which contains at least three parts, including the top level"
    url = pattern(pattern_url)
    "Uniform resource locator addresses"
    btc = alphabet('[a-km-zA-HJ-NP-Z0-9]', prefix=R'(?<!\w)[13]', at_least=26, at_most=33)
    "Bitcoin addresses"
    pem = pattern(pattern_pem)
    "A pattern matching PEM encoded cryptographic parameters"
    xmr = alphabet('[1-9A-HJ-NP-Za-km-z]', prefix='4[0-9AB]', at_least=90, at_most=120)
    "Monero addresses"
    path = pattern(pattern_path)
    "Windows and Linux path names"
    evar = pattern(pattern_win_env_variable)
    "Windows environment variables, i.e. something like `%APPDATA%`"


class defanged(PatternEnum):
    """
    An enumeration of patterns for defanged indicators. Used only by the reverse
    operation of `refinery.defang`.
    """
    hostname = pattern(pattern_hostname_df)
    "A defanged `refinery.lib.patterns.indicators.hostname`."
    url = pattern(pattern_url_df)
    "A defanged `refinery.lib.patterns.indicators.url`."
