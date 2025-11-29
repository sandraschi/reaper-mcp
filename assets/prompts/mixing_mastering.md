# Mixing & Mastering Guide - Reaper-MCP

## Professional Mix Workflow

### Mix Preparation

#### **Organization**
```
Track Groups:
- Drums (color: red)
- Bass (color: orange)
- Guitars (color: yellow)
- Keys/Synths (color: green)
- Vocals (color: blue)
- FX/Ambient (color: purple)
```

#### **Gain Staging**
```
Target levels before mixing:
- Individual tracks: Peak -18dB to -12dB
- Busses: Peak -12dB to -6dB
- Master: Peak -6dB to -3dB (leave headroom)
```

### Mixing Process

#### **Step 1: Balance** (Volume/Panning)
```python
# Solo-in-context method
solo_track(1)  # Kick
# Adjust level
solo_track(2)  # Add snare
# Balance against kick
# Continue adding elements
```

#### **Step 2: EQ**
```
General approach:
- Subtractive first (remove mud, resonances)
- Additive second (enhance character)
- HPF on most tracks (except kick, bass)
- Check in context (solo can lie)
```

#### **Step 3: Compression**
```
Drum compression:
- Kick: 4:1, fast attack, medium release
- Snare: 4:1-6:1, medium attack, fast release
- Parallel compression for punch

Vocal compression:
- 3:1-4:1 ratio
- Medium attack (let transients through)
- Auto release
```

#### **Step 4: Effects**
```
Reverb:
- Short for drums (room, 0.8-1.5s)
- Medium for instruments (hall, 1.5-2.5s)
- Long for vocals (hall/plate, 2-4s)

Delay:
- Sync to tempo
- Hi-pass to prevent mud
- Lower in mix (subtle)
```

### Automation

#### **Dynamic Mixing**
```
Automate:
- Vocal rides (maintain consistent level)
- Effect sends (intro/verse/chorus variations)
- Panning (movement, interest)
- Mutes (clean up between sections)
```

### Mastering Workflow

#### **Mastering Chain** (Typical Order)
```
1. EQ (gentle, broad corrections)
2. Compression (glue, 1.5:1-2:1, subtle)
3. Multiband compression (tighten low-end)
4. Saturation/Exciter (harmonic enhancement)
5. Limiter (loudness, prevent clipping)
6. Metering (check LUFS, true peak)
```

#### **Target Loudness**
```
Genre-dependent LUFS targets:
- Classical/Jazz: -16 to -20 LUFS
- Rock/Pop: -10 to -14 LUFS
- Electronic/Hip-Hop: -8 to -12 LUFS
- Streaming optimized: -14 LUFS

Always check true peak: < -1dB TP
```

### Reaper-MCP Mix Commands

```python
# Track control
mute_track(track=3)
solo_track(track=5)
unsolo_all()

# Bulk operations
mute_all()
unmute_all()

# Session management
save_project()

# Render/Export
# (Use Reaper's render dialog for full control)
```

---

## Mix Checklist

**Balance Phase**:
- ✅ All tracks at proper levels
- ✅ Panning creates width
- ✅ Low-end centered
- ✅ Headroom maintained

**Processing Phase**:
- ✅ EQ removes problems
- ✅ Compression controls dynamics
- ✅ Effects enhance, not dominate
- ✅ Automation adds movement

**Mastering Phase**:
- ✅ Mix sounds finished before mastering
- ✅ Gentle processing (1-2dB max changes)
- ✅ Loudness appropriate for genre
- ✅ True peak safe for distribution

---

**Austrian Quality**: Precision in every decision, transparency in every process, excellence in every result!

