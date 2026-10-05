"""Build the Munajjam benchmark dataset from EveryAyah verse-by-verse files.

One command:  python scripts/build_dataset.py
Quick test:   python scripts/build_dataset.py --surahs 112 --reciters Alafasy_128kbps

For each reciter and surah it
  1. downloads every ayah file (cached in work/, never committed),
  2. decodes each to WAV so durations are exact sample counts,
  3. concatenates them into one WAV per surah,
  4. takes start/end of each ayah from cumulative durations,
  5. measures lead/trail silence per ayah,
  6. writes data/boundaries.csv and data/sources.csv.
"""
import argparse, csv, hashlib, json, re, subprocess, sys, wave
import urllib.request
from pathlib import Path

BASE = "https://everyayah.com/data"
# Placeholders: replace with your 3 reciters (slow / medium / fast) after verifying the folders exist.
RECITERS = ["Minshawy_Murattal_128kbps", "Alafasy_128kbps", "Saood_ash-Shuraym_128kbps"]
AYAH_COUNT = {1: 7, 12: 111, 36: 83, 55: 78, 56: 96, 67: 30, 78: 40, 93: 11, 103: 3, 112: 4}
WORK, DATA = Path("work"), Path("data")
SAMPLE_RATE = 44100  # every ayah is decoded to mono PCM at this rate before concatenation


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr}")
    return r


def download(url, dest):
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "munajjam-benchmark"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as f:
            f.write(resp.read())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration,size:stream=codec_name,bit_rate,sample_rate,channels",
               "-of", "json", str(path)]).stdout
    j = json.loads(out)
    return j["format"], j["streams"][0]


def wav_seconds(path):
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def silences(wav, dur):
    """Return (lead, trail) silence in seconds using ffmpeg silencedetect."""
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav),
               "-af", "silencedetect=noise=-40dB:d=0.02", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    lead = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    trail = 0.0
    if starts and (len(starts) > len(ends) or ends[-1] >= dur - 0.02):
        trail = max(0.0, dur - starts[-1])
    return lead, trail


def cbr_or_vbr(fmt, stream):
    nominal = int(stream.get("bit_rate") or 0)
    avg = int(fmt["size"]) * 8 / float(fmt["duration"])
    return "CBR" if nominal and abs(avg - nominal) / nominal < 0.02 else "VBR"  # heuristic


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reciters", nargs="*", default=RECITERS)
    ap.add_argument("--surahs", nargs="*", type=int, default=list(AYAH_COUNT))
    args = ap.parse_args()
    DATA.mkdir(exist_ok=True)

    bounds, sources = [], []
    for reciter in args.reciters:
        for s in args.surahs:
            wavs = []
            t = 0.0
            for a in range(1, AYAH_COUNT[s] + 1):
                url = f"{BASE}/{reciter}/{s:03d}{a:03d}.mp3"
                mp3 = WORK / reciter / f"{s:03d}{a:03d}.mp3"
                wav = mp3.with_suffix(".wav")
                download(url, mp3)
                if not wav.exists():
                    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
                         "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", str(wav)])
                dur = wav_seconds(wav)
                lead, trail = silences(wav, dur)
                digest = sha256(mp3)
                fmt, st = probe(mp3)
                bounds.append([reciter, s, a, round(t, 6), round(t + dur, 6),
                               round(lead, 4), round(trail, 4), url, digest])
                sources.append([reciter, s, a, fmt.get("size"), st.get("codec_name"),
                                st.get("bit_rate"), st.get("sample_rate"), st.get("channels"),
                                cbr_or_vbr(fmt, st), url, digest])
                t += dur
                wavs.append(wav)

            lst = WORK / reciter / f"{s:03d}.txt"
            lst.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
            full = WORK / reciter / f"{s:03d}_full.wav"
            run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                 "-i", str(lst), "-c", "copy", str(full)])
            total = float(probe(full)[0]["duration"])
            assert abs(bounds[-1][4] - total) <= 0.010, \
                f"{reciter} {s}: last end {bounds[-1][4]} vs file {total}"
            print(f"ok {reciter} surah {s}: {total:.3f}s")

    with open(DATA / "boundaries.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reciter", "surah", "ayah", "start", "end", "lead_silence",
                    "trail_silence", "source_url", "sha256"])
        w.writerows(bounds)
    with open(DATA / "sources.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reciter", "surah", "ayah", "size_bytes", "codec", "bit_rate",
                    "sample_rate", "channels", "cbr_or_vbr", "source_url", "sha256"])
        w.writerows(sources)


if __name__ == "__main__":
    main()
