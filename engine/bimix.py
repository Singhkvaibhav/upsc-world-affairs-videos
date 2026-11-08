"""Bilingual audio for World Affairs: two mixes (English, Hindi) on an identical music + effects bed,
and two subtitle files. Original synthesised sound only: muted marimba bed, teleprinter tick, stamp, pluck."""
import numpy as np, wave, re
from engine.core import TOTAL, LEAD

SR = 44100
N = int(TOTAL*SR)

def _read(fn):
    with wave.open(fn) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
        sr = w.getframerate()
    tn = np.arange(int(len(a)*SR/sr))/SR
    return np.interp(tn, np.arange(len(a))/sr, a).astype(np.float32)

def voice_track(tl, d):
    v = np.zeros(N, np.float32)
    for b in tl:
        a = _read(f"{d}/{b['i']:02d}_{b['k']}.wav")
        s = int((b['start']+LEAD)*SR); v[s:s+len(a)] += a[:N-s]
    return v*(0.89/np.max(np.abs(v)))

def hz(n): return 440*2**((n-69)/12)

def bed():
    t = np.arange(N)/SR
    out = np.zeros(N, np.float32)
    # low pad: two soft sine chords, slow swell (Dm9 - Bbmaj7 - Fmaj7 - C6)
    chords = [[38, 50, 53, 57, 64], [34, 50, 53, 57, 62], [41, 48, 52, 57, 60], [36, 48, 52, 55, 57]]
    CL = 12.0
    for ci in range(int(TOTAL/CL)+2):
        s0 = ci*CL-2; i0, i1 = max(0, int(s0*SR)), min(N, int((s0+CL+4)*SR))
        if i0 >= i1: continue
        tt = t[i0:i1]-s0; env = np.clip(tt/4, 0, 1)*np.clip((CL+4-tt)/4, 0, 1); env = env*env*(3-2*env)
        seg = np.zeros(i1-i0, np.float32)
        for n in chords[ci % 4]: seg += np.sin(2*np.pi*hz(n)*t[i0:i1]).astype(np.float32)*(0.6 if n < 45 else 0.35)
        out[i0:i1] += seg*env*0.5
    # muted marimba: pentatonic notes every ~0.75 s, gentle
    rng = np.random.default_rng(4)
    scale = [62, 65, 67, 69, 72, 74, 77]
    step = 0.75; L = int(1.2*SR); tt = np.arange(L)/SR
    for k in range(int(TOTAL/step)):
        if rng.random() < 0.45: continue
        n = scale[rng.integers(len(scale))]; f = hz(n)
        note = (np.sin(2*np.pi*f*tt) + .3*np.sin(2*np.pi*4*f*tt)*np.exp(-tt*25))*np.exp(-tt*6)
        i0 = int(k*step*SR); j = min(L, N-i0)
        out[i0:i0+j] += note[:j].astype(np.float32)*rng.uniform(.25, .45)
    out /= np.max(np.abs(out))
    fade = np.clip(t/3, 0, 1)*np.clip((TOTAL-t)/4, 0, 1)
    return (out*fade).astype(np.float32)

def fx_sound(kind):
    if kind == 'tick':      # teleprinter: a few quick clicks
        L = int(.5*SR); s = np.zeros(L, np.float32); rng = np.random.default_rng(2)
        for k in range(7):
            i = int(k*.06*SR); n = int(.008*SR)
            s[i:i+n] += (rng.standard_normal(n)*np.exp(-np.arange(n)/30)).astype(np.float32)
        return s*.5
    if kind == 'stamp':     # muffled thunk
        tt = np.arange(int(.35*SR))/SR; rng = np.random.default_rng(1)
        return (np.sin(2*np.pi*80*tt)*np.exp(-tt*22) + .5*rng.standard_normal(len(tt))*np.exp(-tt*70)).astype(np.float32)
    if kind == 'pluck':     # Karplus-Strong string
        f = hz(67); n = int(SR/f); L = int(1.6*SR); rng = np.random.default_rng(3)
        buf = rng.uniform(-1, 1, n); out = np.zeros(L, np.float32)
        for i in range(L):
            out[i] = buf[i % n]; buf[i % n] = .996*.5*(buf[i % n] + buf[(i+1) % n])
        return out
    raise ValueError(kind)

def effects(tl, spec):
    st = {b['k']: b['start'] for b in tl}; bb = {b['k']: b for b in tl}; out = np.zeros(N, np.float32)
    for kind, beat, off, gain in spec:
        if isinstance(off, str):   # a phrase in the English narration
            b = bb[beat]; off = LEAD + b['vo']*b['narr'].find(off)/len(b['narr'])
        s = fx_sound(kind); s = s/np.max(np.abs(s))*gain
        i0 = int((st[beat]+off)*SR); j = min(len(s), N-i0); out[i0:i0+j] += s[:j]
    return out

def _write(fn, mix):
    mix = np.tanh(mix*1.05)/np.tanh(1.05); st = np.stack([mix, mix], 1)
    with wave.open(fn, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1)*32767).astype(np.int16).tobytes())

def _ts(x):
    h, m = int(x//3600), int(x % 3600//60); s = x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)) % 1000:03d}"

def _chunks(text, maxc=90):
    sents = [s for s in re.split(r'(?<=[.?!।])\s+', text.strip()) if s]
    out = []
    for s in sents:
        while len(s) > maxc*1.5:
            m = len(s)//2; cands = [x.end() for x in re.finditer(r', |; |: ', s)]
            cut = min(cands, key=lambda c: abs(c-m)) if cands else m
            out.append(s[:cut].strip()); s = s[cut:].strip()
        out.append(s)
    return out

def srt(tl, texts, durkey, fn):
    n = 0
    with open(fn, 'w', encoding='utf-8') as f:
        for b in tl:
            text = texts[b['k']]; d = b[durkey]; parts = _chunks(text); L = len(text); pos = 0
            for j, p in enumerate(parts):
                s0 = b['start'] + LEAD + d*pos/L; pos += len(p)+1
                e0 = b['start'] + LEAD + d*pos/L + (0.3 if j == len(parts)-1 else 0)
                n += 1; f.write(f"{n}\n{_ts(s0)} --> {_ts(e0)}\n{p}\n\n")

def build2(tl, fx_spec, HI, name):
    b0 = bed(); fx = effects(tl, fx_spec)
    for lang, d in (('en', 'vo'), ('hi', 'vo_hi')):
        v = voice_track(tl, d)
        env = np.convolve(np.abs(v), np.ones(4410)/4410, mode='same')
        duck = 1 - 0.5*np.clip(env*12, 0, 1)
        _write(f'mix_{lang}.wav', v + b0*0.07*duck + fx)
    srt(tl, {b['k']: b['narr'] for b in tl}, 'vo', f'{name}.en.srt')
    srt(tl, HI, 'vo_hi', f'{name}.hi.srt')
    print('ok two mixes', TOTAL)
