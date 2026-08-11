import pytest

from audio_processing.transcript_cleaner import (
    clean_text,
    collapse_repeated_words,
    normalize_whitespace,
    remove_filler_words,
    preserve_technical_terms,
)


def test_normalize_whitespace():
    assert normalize_whitespace("  hello   world\n\t") == "hello world"


def test_remove_filler_words():
    assert remove_filler_words("um this is uh a test", {"um", "uh"}) == "this is a test"


def test_collapse_repeated_words():
    assert collapse_repeated_words("this this is is a test test") == "this is a test"


def test_preserve_technical_terms():
    text = "a cnn model uses transformer attention"
    assert preserve_technical_terms(text, ["CNN", "Transformer", "attention"]) == "a CNN model uses Transformer attention"


def test_clean_text_preserves_meaning_and_tech_terms():
    text = "um, so we are looking at CNN and python recursion, uh with gradient descent."
    cleaned = clean_text(text, {"um", "so", "uh"}, ["CNN", "python", "recursion", "gradient descent"])
    assert "CNN" in cleaned
    assert "python" in cleaned
    assert "recursion" in cleaned
    assert "gradient descent" in cleaned
    assert "um" not in cleaned.lower()
    assert "uh" not in cleaned.lower()


def test_clean_text_collapses_repeated_words():
    text = "this is is a a test"
    cleaned = clean_text(text, set(), [])
    assert cleaned == "this is a test"


def test_clean_text_normalizes_punctuation_spacing():
    text = "hello , world ! this is a test ."
    cleaned = clean_text(text, set(), [])
    assert cleaned == "hello, world! this is a test."
