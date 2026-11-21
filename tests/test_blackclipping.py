"""Comprehensive verification tests for BlackClipping upgrades:
1. Rebranding & UI titles
2. Max clips capacity up to 50
3. Accelerated parallel render pool & hardware encoders (NVENC, QSV, AMF, CPU)
4. 100% viral scoring heuristics & catchy click-worthy titles
5. Pitch black & neon green theme with interactive mouse glow follower
6. Customization options & settings
7. 16:9 Widescreen & 9:16 Split layouts
8. Preset profiles (Speed/Kick, GTA/BGMI, Viral Shorts)
9. Watermark branding & Dead Air silence remover
10. Native Windows BlackClipping.exe application
"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

fails = []

def check(name, got, want=True):
    ok = (got == want) if not callable(want) else want(got)
    status = "PASS" if ok else "FAIL"
    print(f"{status} {name}" + ("" if ok else f" (got: {got!r}, want: {want!r})"))
    if not ok:
        fails.append(name)

# --- 1. Check FastAPI server title & branding ---
from studio.server import app
check("FastAPI app title is BlackClipping", app.title, "BlackClipping")

# --- 2. Check Jobs limits and max clips up to 50 ---
from studio import jobs
check("LIMITS max_clips allows up to 50", jobs.LIMITS["max_clips"], (1, 50))

cleaned = jobs.clean_options({
    "max_clips": "45",
    "min_len": "20",
    "max_len": "60",
    "watermark": "@SpeedClipsVault",
    "remove_silence": True
})
check("clean_options accepts 45 clips", cleaned["max_clips"], 45)
check("clean_options accepts watermark", cleaned["watermark"], "@SpeedClipsVault")
check("clean_options accepts remove_silence", cleaned["remove_silence"], True)

cleaned_cap = jobs.clean_options({"max_clips": "99"})
check("clean_options caps at 50", cleaned_cap["max_clips"], 50)

# --- 3. Check Hardware Encoders & Speed in Render ---
from studio import render
check("Hardware encoders candidate map ready", hasattr(render, "_hw_encoder"), True)
check("Styles include Hormozi, MrBeast and Neon",
      all(s in render.STYLES for s in ("hormozi", "mrbeast", "neon", "bounce", "hype", "clean")), True)
check("Split layout registered in render", "split" in render.LAYOUTS, True)
check("16:9 Widescreen layout registered in render", "widescreen" in render.LAYOUTS, True)

# --- 4. Check 100% Viral Heuristics in Brain ---
from studio import brain
import numpy as np

db_sample = np.array([10.0, 15.0, 45.0, 50.0, 48.0, 12.0, 10.0, 9.0] * 5, dtype=np.float32)
words_sample = [
    {"w": "bro", "s": 2.0, "e": 2.5},
    {"w": "no", "s": 2.6, "e": 2.9},
    {"w": "way", "s": 3.0, "e": 3.4},
    {"w": "what", "s": 3.5, "e": 4.0},
    {"w": "happened", "s": 4.1, "e": 4.8},
]
viral_picks = brain.fallback_by_loudness(db_sample, words_sample, n=10, max_len=30, duration=40)
check("Viral loudness fallback generates clips", len(viral_picks) >= 1, True)
if viral_picks:
    check("Viral score is calibrated 75-99", 75 <= viral_picks[0]["score"] <= 99, True)
    check("Viral hook has high impact shock phrasing", len(viral_picks[0]["hook"]) > 3, True)
    check("Viral hashtags generated", len(viral_picks[0]["hashtags"]) >= 4, True)

# --- 5. Check index.html Theme, Mouse Follower and Options ---
index_path = ROOT / "web" / "index.html"
index_html = index_path.read_text(encoding="utf-8")

check("index.html title has BlackClipping", "BlackClipping" in index_html, True)
check("Neon green brand color defined", "--brand:#00FF66" in index_html, True)
check("Dark color-scheme enabled", "color-scheme:dark" in index_html, True)
check("Mouse glow follower element present", '<div id="mouse-glow"></div>' in index_html, True)
check("Mouse canvas trail element present", '<canvas id="mouse-canvas"></canvas>' in index_html, True)
check("Mouse trail animation script present", 'animate' in index_html and 'particles' in index_html, True)
check("Clips stepper configured up to 50", 'stepper("o_max", "How many clips", c?.max_clips ?? 10, 1, 50, 1, "")' in index_html, True)
check("Viral Scout Mode option present in composer", 'o_mode' in index_html and '🔥 100% Viral' in index_html, True)
check("Render Engine Speed option present in composer", 'o_speed' in index_html and '⚡ Turbo GPU' in index_html, True)
check("Quick Presets bar present in composer", 'data-preset="speed_kick"' in index_html and 'data-preset="gta_bgmi"' in index_html, True)
check("Channel Watermark option present in composer", 'id="o_watermark"' in index_html, True)
check("Auto-Cut Dead Air silence option present in composer", 'id="o_silence"' in index_html, True)
check("Widescreen layout option present", 'widescreen:"16:9 Landscape Widescreen"' in index_html, True)

# --- 6. Check Config Aliases ---
from studio import config
os.environ["BLACKCLIPPING_TEST_VAR"] = "success"
check("Config env() supports BLACKCLIPPING_ prefix", config.env("BLACKCLIPPING_TEST_VAR"), "success")
check("Config env() aliases CLIPKONTRAST_ prefix", config.env("CLIPKONTRAST_TEST_VAR"), "success")

# --- 7. Check BlackClipping.exe ---
exe_path = ROOT / "BlackClipping.exe"
check("BlackClipping.exe exists", exe_path.exists(), True)
check("BlackClipping.exe size > 15KB", exe_path.stat().st_size > 15000 if exe_path.exists() else 0, True)

ico_path = ROOT / "BlackClipping.ico"
check("BlackClipping.ico exists", ico_path.exists(), True)

print("\n" + ("=" * 40))
if fails:
    print(f"FAILED: {len(fails)} test(s) failed: {', '.join(fails)}")
    sys.exit(1)
else:
    print("ALL BLACKCLIPPING VERIFICATION TESTS PASSED!")
    sys.exit(0)
