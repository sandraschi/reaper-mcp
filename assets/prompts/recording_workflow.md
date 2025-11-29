# Recording Workflow - Reaper-MCP

## Professional Recording Session Workflow

### Pre-Session Setup

#### **1. Project Configuration**
```
- Set sample rate (44.1kHz/48kHz/96kHz)
- Configure bit depth (24-bit recommended)
- Create project folder structure
- Set default track count
- Configure monitoring (input monitoring enable)
```

#### **2. Track Preparation**
```python
# Typical multi-track session setup
Tracks:
1. Kick
2. Snare
3. Hi-hat
4. Overheads (stereo, tracks 4-5)
6-8. Toms
9-10. Bass DI + Amp
11-20. Guitars, keys, etc.
21+. Vocals

# Arm tracks for recording
arm_track(track=1)
arm_track(track=2)
# ... etc
```

#### **3. Input Routing**
```
- Verify audio interface inputs
- Set input channels per track
- Enable input monitoring where needed
- Check phantom power (condensers)
- Set initial gain staging (-18dB to -12dB peaks)
```

### Recording Best Practices

#### **Gain Staging**
```
Target levels:
- Peaks: -12dB to -6dB (leave headroom)
- RMS: -18dB to -14dB
- Never clip (0dB)
- Quieter sources: boost at interface, not in DAW
```

#### **Take Management**
```
Workflow:
1. Record Take 1
2. Add marker "Take 1"
3. Stop, review
4. Record Take 2 (keep previous takes)
5. Comp best sections later

Reaper advantages:
- Non-destructive recording
- Automatic take lanes
- Easy comp editing
```

#### **Session Organization**
```
Markers for:
- Song sections (Intro, Verse 1, Chorus, etc.)
- Takes (Take 1, Take 2, Best Take)
- Issues (Fix this, Re-record, Check tuning)
- Reference points (Start here tomorrow)
```

### Live Recording Scenarios

#### **Band Recording**
```
Setup:
1. All musicians in place
2. All tracks armed
3. Monitoring configured (musician mixes)
4. Reference track/click loaded
5. Markers for song structure

Execution:
1. Start recording
2. Monitor all tracks for issues
3. Stop at end or on issue
4. Review immediately
5. Re-record if needed
```

#### **Vocal Recording**
```
Setup:
- Comp mic (Neumann, AKG, etc.)
- Pop filter
- Monitoring (with effects for performer, dry for recording)
- Pitch reference track
- Lyrics/cue system

Multiple Takes:
- Record 3-5 complete takes
- Mark standout sections
- Comp best performance later
```

#### **Instrument Overdubs**
```
Workflow:
1. Solo existing tracks for reference
2. Arm new track
3. Enable metronome/click if needed
4. Record multiple takes
5. Quick review
6. Move to next part
```

### Monitoring During Recording

#### **Reaper-MCP Monitoring**
```python
# Check transport status
status = get_transport_status()

# Verify tracks armed
for track in [1, 2, 3, 4]:
    is_armed = get_track_arm_status(track)
    
# During recording
# Monitor levels visually
# Listen for issues (clicks, pops, distortion)
```

#### **What to Listen For**
- Clipping/distortion
- Unwanted noise (hum, buzz, background)
- Timing issues
- Tuning problems
- Performance mistakes
- Technical glitches

### Post-Recording

#### **Immediate Review**
```
After each take:
1. Playback immediately
2. Check for technical issues
3. Evaluate performance
4. Decide: Keep, Re-record, or Move on
5. Add markers/notes
```

#### **Session Cleanup**
```
End of session:
1. Mute/delete unusable takes
2. Rename tracks appropriately
3. Color-code track groups
4. Add markers for next session
5. Save project (multiple backups!)
6. Export rough mix for review
```

### Reaper-MCP Recording Commands

#### **Essential Commands**
```python
# Start recording
record()

# Stop recording
stop()

# Playback for review
play()

# Go to marker
go_to_marker(marker_name="Verse 1")

# Save project
save_project()

# Add marker at current position
add_marker(name="Great take!")
```

---

## Recording Checklist

**Before Recording**:
- ✅ Inputs configured and tested
- ✅ Tracks armed
- ✅ Monitoring working
- ✅ Levels appropriate (-18dB to -12dB)
- ✅ Project saved

**During Recording**:
- ✅ Monitor for clipping
- ✅ Watch for technical issues
- ✅ Note good/bad takes
- ✅ Communicate with performers

**After Recording**:
- ✅ Review immediately
- ✅ Add markers/notes
- ✅ Save project
- ✅ Backup if important session
- ✅ Export reference mix

---

**Austrian Precision**: Prepare thoroughly, record cleanly, organize meticulously. Quality starts at the recording stage!

