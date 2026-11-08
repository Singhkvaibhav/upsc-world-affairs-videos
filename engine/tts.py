import wave, json, re, io, sys
import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

def run(beats, voice_path):
    v = PiperVoice.load(voice_path)
    cfg = SynthesisConfig(length_scale=1.22, noise_scale=0.55, noise_w_scale=0.7)
    SR = v.config.sample_rate
    def synth(t):
        b = io.BytesIO()
        with wave.open(b, "wb") as w: v.synthesize_wav(t, w, syn_config=cfg)
        b.seek(0)
        with wave.open(b) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16)
    durs = {}
    for i, (k, txt) in enumerate(beats):
        parts = [p for p in re.split(r'(?<=[.?!:])\s+', txt) if p]
        out = []
        for j, p in enumerate(parts):
            a = synth(p)
            nz = np.where(np.abs(a) > 300)[0]
            if len(nz): a = a[max(0, nz[0]-800): nz[-1]+1600]
            out.append(a)
            if j < len(parts)-1:
                out.append(np.zeros(int(SR*(0.55 if p.endswith(('.', '?', '!')) else 0.35)), np.int16))
        a = np.concatenate(out)
        with wave.open(f"vo/{i:02d}_{k}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
        durs[k] = len(a)/SR
    json.dump(durs, open("vo/durs.json", "w"), indent=1)
    print(SR, round(sum(durs.values()), 1))
