# -*- coding: utf-8 -*-

"Utility Functions"
import locale


def substr(s, start, length=-1):
    if length < 0:
        length = len(s) - start
    return s[start : start + length]


def sprintf(fmt, *args):
    return fmt % args


def UTF8ToUTF16BE(instr, setbom=True):
    "Converts UTF-8 strings to UTF16-BE."
    outstr = b""
    if setbom:
        outstr += "\xFE\xFF".encode("latin1")
    if not isinstance(instr, str):
        instr = instr.decode("UTF-8")
    return outstr + instr.encode("UTF-16BE")


def UTF8StringToArray(instr):
    "Converts UTF-8 strings to codepoints array"
    return [ord(c) for c in instr]


def enclose_in_parens(s):
    "Format a text string"
    if s:
        assert isinstance(s, str)
        return "(" + escape_parens(s) + ")"
    return ""


def escape_parens(s):
    "Add a backslash character before , ( and )"
    if isinstance(s, str):
        return (
            s.replace("\\", "\\\\")
            .replace(")", "\\)")
            .replace("(", "\\(")
            .replace("\r", "\\r")
        )
    return (
        s.replace(b"\\", b"\\\\")
        .replace(b")", b"\\)")
        .replace(b"(", b"\\(")
        .replace(b"\r", b"\\r")
    )


# shortcut to bytes conversion (b prefix)
def b(s):
    if isinstance(s, str):
        return s.encode("latin1")
    if isinstance(s, int):
        return bytes([s])  # http://bugs.python.org/issue4588
    raise ValueError("Invalid input: {}".format(s))


def dochecks():
    # Check for locale-related bug
    # if (1.1==1):
    #     raise FPDFException("Don\'t alter the locale before including class file")
    # Check for decimal separator
    if sprintf("%.1f", 1.0) != "1.0":
        locale.setlocale(locale.LC_NUMERIC, "C")


# Moved here from FPDF#__init__
dochecks()
