"""Tests for viral clipping algorithms, new styles, split layout, and direct live URL support."""
import re
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from studio import brain, live, media, render, jobs, config


def test_styles():
    for style in ("bounce", "hype", "clean", "hormozi", "mrbeast", "neon"):
        assert style in render.STYLES, f"Style {style} missing"
        st = render.STYLES[style]
        assert "font" in st and "size" in st and "base" in st and "active" in st
        assert st["outline"] >= 5
    print("PASS all viral styles (hormozi, mrbeast, neon, bounce, hype, clean) registered")


def test_layouts():
    assert "split" in render.LAYOUTS
    assert "gameplay" in render.LAYOUTS
    assert "blur" in render.LAYOUTS
    assert "crop" in render.LAYOUTS

    # Geometry tests
    layout, fg_h, hook_y, cap_y = render.geometry(1920, 1080, "split")
    assert layout == "split"
    assert fg_h == 1040
    assert hook_y == 160
    assert cap_y == 1420

    # Filter generation
    fc = [100, 50, 400, 300]
    flt = render._filter("split", fg_h, fc)
    assert "vstack=inputs=2" in flt
    assert "crop=400:300:100:50" in flt
    print("PASS split layout geometry and dual-feed vertical stack filter")


def test_viral_categories_and_prompt():
    for cat in ("funny", "clutch", "fail", "shock", "rage", "take", "story", "epic", "satisfying", "debate"):
        assert cat in brain.CATEGORIES, f"Category {cat} missing"
    assert "viral" in brain.HEAD.lower()
    assert "score" in brain.RULES.lower()
    print("PASS viral categories and AI scout prompt heuristics")


def test_fallback_by_loudness():
    words = [
        {"w": "haha", "s": 10.0, "e": 10.5},
        {"w": "that", "s": 10.6, "e": 11.0},
        {"w": "was", "s": 11.1, "e": 11.4},
        {"w": "so", "s": 11.5, "e": 11.7},
        {"w": "funny", "s": 11.8, "e": 12.2},
    ]
    import numpy as np
    db = np.zeros(60, dtype=np.float32)
    db[10:15] = -5.0  # loud peak
    db[20:] = -40.0
    picks = brain.fallback_by_loudness(db, words, n=2, max_len=30, duration=60.0)
    assert len(picks) > 0
    pick = picks[0]
    assert pick["score"] >= 50
    assert pick["category"] in brain.CATEGORIES
    assert pick["hook"]
    assert len(pick["hashtags"]) >= 3
    print("PASS smart viral loudness fallback with contextual category detection")


def test_live_normalization_and_detection():
    # YouTube channel live
    yt_chan = "https://www.youtube.com/@IShowSpeed"
    norm_yt = live.normalize(yt_chan)
    assert norm_yt == "https://www.youtube.com/@IShowSpeed/live"

    # Direct Twitch channel
    tw_chan = "https://www.twitch.tv/shroud"
    norm_tw = live.normalize(tw_chan)
    assert "twitch.tv/shroud" in norm_tw

    # Kick channel
    kick_chan = "https://kick.com/xqc"
    norm_kick = live.normalize(kick_chan)
    assert "kick.com/xqc" in norm_kick

    # Speech triggers
    assert brain.roman.to_roman("HELLO WORLD") == "HELLO WORLD"
    match = live.Session.CLIP_WORDS.search("oh my god clip that right now")
    assert match is not None
    print("PASS live URL normalization and viral speech reaction triggers")


def main():
    test_styles()
    test_layouts()
    test_viral_categories_and_prompt()
    test_fallback_by_loudness()
    test_live_normalization_and_detection()
    print("ALL VIRAL & LIVE TESTS PASSED")


if __name__ == "__main__":
    main()
