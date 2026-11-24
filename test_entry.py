import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_CHARS = 200


def test_entry():
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
        r = subprocess.run(
            [sys.executable, os.path.join(HERE, "main.py")],
            env=env, capture_output=True, text=True, timeout=60,
        )
        assert r.returncode == 0, r.stderr
        with open(os.path.join(tmp, "entry.txt"), encoding="utf-8") as f:
            content = f.read()
    lines = content.strip().splitlines()
    assert len(lines) == 1, f"expected exactly 1 line, got {len(lines)}"
    text = lines[0]
    assert 1 <= len(text) <= MAX_CHARS, f"length {len(text)} outside 1-{MAX_CHARS}"
    assert text.strip(), "entry must not be blank"
    print(f"ok: 1 line, {len(text)} chars: {text}")


if __name__ == "__main__":
    test_entry()
