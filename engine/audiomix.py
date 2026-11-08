import numpy as np, wave
from engine.core import TOTAL, LEAD

def build(tl, fx_spec, srt_name):
    SR = 44100
    N = int(TOTAL*SR)

    def read(fn):
        with wave.open(fn) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
            sr = w.getframerate()
        t_new = np.arange(int(len(a)*SR/sr))/SR
        return np.interp(t_new, np.arange(len(a))/sr, a)

    voice = np.zeros(N, np.float32)
    for b in tl:
        a = read(f"vo/{b['i']:02d}_{b['k']}.wav")
        s = int((b['start']+LEAD)*SR)
        voice[s:s+len(a)] += a[:N-s]
    voice *= 0.89/np.max(np.abs(voice))

    # --- ambient pad ---
    t = np.arange(N)/SR
    def hz(n): return 440*2**((n-69)/12)
    chords = [[45, 52, 57, 60], [41, 48, 53, 57], [48, 52, 55, 60], [43, 50, 55, 59]]  # Am F C G
    CL = 10.0
    pad = np.zeros(N, np.float32)
    for ci in range(int(TOTAL/CL)+2):
        ch = chords[ci % 4]
        s0 = ci*CL - 2.0
        i0, i1 = max(0, int(s0*SR)), min(N, int((s0+CL+4)*SR))
        if i0 >= i1: continue
        tt = t[i0:i1]-s0
        env = np.clip(tt/3.0, 0, 1)*np.clip((CL+4-tt)/3.0, 0, 1)
        env = env*env*(3-2*env)
        seg = np.zeros(i1-i0)
        for n in ch:
            f = hz(n)
            for det in (-0.12, 0.12):
                seg += np.sin(2*np.pi*(f+det)*t[i0:i1]) + 0.25*np.sin(2*np.pi*2*(f+det)*t[i0:i1]+1)
        pad[i0:i1] += seg*env
    pad *= (0.8+0.2*np.sin(2*np.pi*t/13))
    pad /= np.max(np.abs(pad))
    # duck under voice
    env_v = np.convolve(np.abs(voice), np.ones(4410)/4410, mode='same')
    duck = 1 - 0.45*np.clip(env_v*12, 0, 1)
    pad *= 0.085*duck
    fade = np.clip(t/3, 0, 1)*np.clip((TOTAL-t)/4, 0, 1)
    pad *= fade

    # --- aurora chime ---
    def chime(at, gain=0.22):
        out = np.zeros(N, np.float32)
        i0 = int(at*SR); L = int(4*SR)
        tt = np.arange(min(L, N-i0))/SR
        sig = np.zeros_like(tt)
        for k, (n, g) in enumerate([(81, 1), (88, .6), (93, .45), (76, .5)]):
            d = 0.12*k
            tk = np.clip(tt-d, 0, None)
            sig += g*np.sin(2*np.pi*hz(n)*tk)*np.exp(-tk*1.6)*(tt >= d) + .2*g*np.sin(2*np.pi*hz(n)*2.76*tk)*np.exp(-tk*4)*(tt >= d)
        out[i0:i0+len(tt)] = sig/np.max(np.abs(sig))*gain
        return out

    def click(at, gain=0.35):
        out = np.zeros(N, np.float32)
        i0 = int(at*SR); L = int(.25*SR)
        tt = np.arange(L)/SR
        rng = np.random.default_rng(1)
        sig = np.sin(2*np.pi*95*tt)*np.exp(-tt*28) + 0.4*rng.standard_normal(L)*np.exp(-tt*60)
        out[i0:i0+L] = sig/np.max(np.abs(sig))*gain
        return out

    st = {b['k']: b['start'] for b in tl}
    fx = np.zeros(N, np.float32)
    for kind, beat, off, *g in fx_spec:
        fx = fx + (chime if kind == 'chime' else click)(st[beat]+off, *g)

    mix = voice + pad + fx
    mix = np.tanh(mix*1.05)/np.tanh(1.05)
    stereo = np.stack([mix, mix], 1)
    with wave.open('mix.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1, 1)*32767).astype(np.int16).tobytes())

    # subtitles
    def ts(x):
        h, m = int(x//3600), int(x % 3600//60); s = x % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
    with open(srt_name, 'w') as f:
        n = 0
        for b in tl:
            if b.get('chunks'):
                for j, (s0, e0, txt) in enumerate(b['chunks']):
                    n += 1; e = e0 if j < len(b['chunks'])-1 else LEAD+b['vo']+0.4
                    f.write(f"{n}\n{ts(b['start']+s0)} --> {ts(b['start']+e)}\n{txt}\n\n")
            else:
                n += 1
                f.write(f"{n}\n{ts(b['start']+LEAD)} --> {ts(b['start']+LEAD+b['vo']+0.4)}\n{b['text']}\n\n")
    print('ok', len(mix)/SR)
