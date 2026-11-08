"""Audio mix: narration, a soft original bed of light hand percussion and plucked strings (all synthesised),
plus effects: thread (needle and thread), cloth (fabric swish), tick (countdown), ding (answer), tab/tab_sam (rhythm clicks)."""
import numpy as np, wave
from engine import core
from engine.core import TOTAL, LEAD

SR = 44100

def _read(fn):
    with wave.open(fn) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
        sr = w.getframerate()
    t_new = np.arange(int(len(a)*SR/sr))/SR
    return np.interp(t_new, np.arange(len(a))/sr, a)

def hz(n): return 440*2**((n-69)/12)

def _put(out, sig, at):
    i0 = int(at*SR)
    if i0 >= len(out) or i0 < 0: return
    n = min(len(sig), len(out)-i0); out[i0:i0+n] += sig[:n]

def pluck(note, dur=2.2, gain=1.):
    t = np.arange(int(dur*SR))/SR; f = hz(note); sig = np.zeros_like(t)
    for h, g in ((1, 1), (2, .5), (3, .32), (4, .2), (5, .12), (6, .07)):
        sig += g*np.sin(2*np.pi*f*h*t*(1+.0004*h*h))*np.exp(-t*(2.2+1.6*h))
    sig *= np.clip(t/.004, 0, 1)
    return sig/np.max(np.abs(sig))*gain

def drum(kind, gain=1.):
    n = int(.5*SR); t = np.arange(n)/SR; rng = np.random.default_rng(3)
    if kind == 'dha':   # low hand-drum
        sig = np.sin(2*np.pi*(78+60*np.exp(-t*30))*t)*np.exp(-t*9)+.12*rng.standard_normal(n)*np.exp(-t*80)
    elif kind == 'tin': # high bright tap
        sig = np.sin(2*np.pi*(340+90*np.exp(-t*40))*t)*np.exp(-t*22)+.08*rng.standard_normal(n)*np.exp(-t*120)
    else:               # shaker tick
        sig = rng.standard_normal(n)*np.exp(-t*90); sig = np.diff(sig, prepend=0)
    return sig/np.max(np.abs(sig))*gain

def fx_sound(kind, gain):
    rng = np.random.default_rng(abs(hash(kind)) % 1000)
    if kind == 'thread':       # a soft needle-and-thread draw: airy sweep with tiny pulls
        n = int(1.6*SR); t = np.arange(n)/SR; x = rng.standard_normal(n)
        x = np.convolve(x, np.ones(18)/18, 'same'); x = np.diff(x, prepend=0)*6
        env = np.sin(np.pi*np.clip(t/1.6, 0, 1))**2*(0.6+0.4*np.sin(2*np.pi*9*t))
        tone = np.sin(2*np.pi*(1400+800*t)*t)*.15
        sig = (x+tone)*env
    elif kind == 'cloth':      # a gentle fabric swish
        n = int(.7*SR); t = np.arange(n)/SR; x = rng.standard_normal(n)
        x = np.convolve(x, np.ones(40)/40, 'same')*5
        sig = x*np.sin(np.pi*np.clip(t/.7, 0, 1))**2
    elif kind == 'tick':       # countdown: soft wooden tap
        n = int(.2*SR); t = np.arange(n)/SR; sig = np.sin(2*np.pi*520*t)*np.exp(-t*38)
    elif kind == 'ding':       # answer: warm plucked chime
        sig = pluck(76, 1.6)+.5*pluck(83, 1.6)
    elif kind == 'tab_sam':
        sig = drum('dha')+.6*drum('tin')
    elif kind == 'tab':
        sig = drum('tin')
    else: sig = np.zeros(10)
    m = np.max(np.abs(sig)); return sig/m*gain if m > 0 else sig

def bed(total, voice_env):
    """Light hand percussion + plucked strings in a gentle pentatonic, ducked under the narration."""
    N = int(total*SR); out = np.zeros(N, np.float32); beat = .75
    pattern = ['dha', None, 'tin', None, 'tin', None, 'dha', 'tin']   # 8 pulses
    n = int(total/beat)
    for i in range(n):
        k = pattern[i % 8]
        if k: _put(out, drum(k, .55 if k == 'dha' else .3), i*beat)
        if i % 2 == 1: _put(out, drum('tick', .12), i*beat+beat/2)
    scale = [62, 64, 66, 69, 71, 74]; rng = np.random.default_rng(8); t0 = 1.0; prev = 2
    while t0 < total-2:
        prev = int(np.clip(prev+rng.integers(-2, 3), 0, len(scale)-1)); _put(out, pluck(scale[prev]-12*(rng.random() < .3), 2.4, .6), t0)
        t0 += rng.choice([1.5, 2.25, 3.0])
    t = np.arange(N)/SR
    drone = (np.sin(2*np.pi*hz(50)*t)+.4*np.sin(2*np.pi*hz(57)*t))*.08*(0.8+.2*np.sin(2*np.pi*t/9))
    out += drone.astype(np.float32)
    out /= max(np.max(np.abs(out)), 1e-6)
    duck = 1-.55*np.clip(voice_env*12, 0, 1)
    fade = np.clip(t/2.5, 0, 1)*np.clip((total-t)/3.5, 0, 1)
    return out*.13*duck*fade

def build(tl, events, srt_name, total=None):
    total = total or TOTAL; N = int(total*SR)
    voice = np.zeros(N, np.float32)
    for b in tl:
        a = _read(f"vo/{b['i']:02d}_{b['k']}.wav"); s = int((b['start']+LEAD)*SR)
        voice[s:s+len(a)] += a[:max(0, N-s)]
    voice *= 0.89/np.max(np.abs(voice))
    env_v = np.convolve(np.abs(voice), np.ones(4410)/4410, mode='same')
    mix = voice+bed(total, env_v)
    fx = np.zeros(N, np.float32)
    for kind, at, g in events: _put(fx, fx_sound(kind, g*.34), at)
    mix = mix+fx*(1-.5*np.clip(env_v*10, 0, 1))
    mix = np.tanh(mix*1.05)/np.tanh(1.05)
    stereo = np.stack([mix, mix], 1)
    with wave.open('mix.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1, 1)*32767).astype(np.int16).tobytes())
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
