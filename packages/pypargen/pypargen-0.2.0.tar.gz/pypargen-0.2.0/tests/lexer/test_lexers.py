# Copyright 2021 Ilango Rajagopal
# Licensed under GPL-3.0-only

import pytest
import io
from pypargen.lexer import pyre, lexer


def palindrome(lexerClass):
    terminals = ['"a"', '"b"']
    input = "aabb"
    inputbuf = io.StringIO(input)
    lexer1 = lexerClass(terminals, inputbuf)
    assert lexer1.terminals == terminals

    tokens = list(lexer1)

    assert ''.join(map(lambda x: x.content, tokens[:-1])) == input

    true_token_types = [0, 0, 1, 1]
    assert [x.type for x in tokens
            ] == [terminals[i] for i in true_token_types] + ['$']


def math(lexerClass):
    terminals = [
        '"[1-9][0-9]*"', r'"\("', r'"\)"', '"/"', r'"\*"', r'"\+"', '"-"'
    ]
    input = "(1+2)/(4-1)"
    inputbuf = io.BytesIO(input.encode())

    if lexerClass == lexer.Lexer:
        terminals[5] = '"+"'
    lexer1 = lexerClass(terminals, inputbuf)
    assert lexer1.terminals == terminals

    tokens = list(lexer1)

    assert ''.join(map(lambda x: x.content, tokens[:-1])) == input

    true_token_types = [1, 0, 5, 0, 2, 3, 1, 0, 6, 0, 2]
    assert [x.type for x in tokens
            ] == [terminals[i] for i in true_token_types] + ['$']


def invalid(lexerClass):
    terminals = ['"a"', '"b"']
    input = "aabxab"
    inputbuf = io.StringIO(input)
    lexer1 = lexerClass(terminals, inputbuf)
    assert lexer1.terminals == terminals

    list(lexer1)


def active(lexerClass):
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    inputstr = "abcAbc"
    inputbuf = io.StringIO(inputstr)
    lexer1 = lexerClass(terminals, inputbuf)
    i = 0

    while (tok := lexer1.nextToken(terminals)).type != '$':
        if i == 3:
            terminals = terminals[1:]
        assert tok.type == terminals[0]
        assert tok.content == inputstr[i]
        i += 1


def active_invalid(lexerClass):
    terminals = ['"[a-z]"', '"[A-Za-z]"']
    inputstr = "abcABC"
    inputbuf = io.StringIO(inputstr)
    lexer1 = lexerClass(terminals, inputbuf)
    i = 0

    while (tok := lexer1.nextToken(terminals)).type != '$':
        assert tok.type == terminals[0]
        assert tok.content == inputstr[i]
        i += 1
        if i == 3:
            terminals = ['"[A-Z]"']
    raise RuntimeError("Should not reach here")


def test_pyre_palindrome():
    palindrome(pyre.PyRELexer)


def test_lexer_palindrome():
    palindrome(lexer.Lexer)


def test_pyre_math():
    math(pyre.PyRELexer)


def test_lexer_palindrom():
    math(lexer.Lexer)


@pytest.mark.xfail(strict=True, raises=pyre.UnexpectedCharacter)
def test_pyre_invalid():
    invalid(pyre.PyRELexer)


@pytest.mark.xfail(strict=True, raises=pyre.UnexpectedCharacter)
def test_lexer_invalid():
    invalid(lexer.Lexer)


def test_pyre_active():
    active(pyre.PyRELexer)


def test_lexer_active():
    active(lexer.Lexer)


@pytest.mark.xfail(strict=True, raises=pyre.UnregisteredTerminal)
def test_pyre_active_invalid():
    active_invalid(pyre.PyRELexer)


@pytest.mark.xfail(strict=True, raises=pyre.UnregisteredTerminal)
def test_lexer_active_invalid():
    active_invalid(lexer.Lexer)
