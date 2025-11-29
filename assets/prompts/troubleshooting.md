# Troubleshooting - Reaper-MCP

## OSC Connection Issues

### Problem: Reaper not responding to MCP commands

**Solutions**:
1. ✅ Verify Reaper is running
2. ✅ Check OSC enabled in Preferences → Control/OSC/web
3. ✅ Confirm ports: 8000 (local listen), 8001 (remote)
4. ✅ Pattern config set to "Default.ReaperOSC"
5. ✅ "Send all feedback" enabled
6. ✅ Firewall allowing UDP ports 8000-8001

### Problem: Intermittent connection drops

**Solutions**:
- Check network stability
- Verify no other apps using ports 8000-8001
- Restart Reaper OSC (disable/enable in preferences)
- Check system firewall/antivirus

## Audio Issues

### Problem: No audio playback

**Checklist**:
1. Audio device configured (Preferences → Audio)
2. Correct output selected
3. Master track not muted
4. Project sample rate matches interface
5. Buffer size appropriate (256-512 samples)

### Problem: Latency/delay

**Solutions**:
- Reduce buffer size (64-128 samples for recording)
- Enable low-latency monitoring
- Use ASIO driver (Windows) or Core Audio (Mac)
- Disable unnecessary plugins
- Freeze/render heavy tracks

### Problem: Clicks, pops, dropouts

**Causes & Solutions**:
- Buffer too small → Increase buffer size
- CPU overload → Freeze tracks, disable plugins
- Disk too slow → Use SSD, defragment
- USB issues → Use quality cables, powered hub

## Recording Issues

### Problem: Can't arm tracks for recording

**Solutions**:
- ✅ Check "Automatically arm tracks" setting
- ✅ Verify input assigned to track
- ✅ Reaper not in stop state (must be stopped or playing)
- ✅ Track not record-locked

### Problem: Recording distorted/clipping

**Solutions**:
- Reduce input gain at interface (primary solution)
- Check for gain plugins on input
- Verify 24-bit recording (not 16-bit)
- Monitor input levels (aim for -18dB to -12dB peaks)

## Reaper-MCP Specific

### Problem: Python OSC server won't start

**Checklist**:
1. Python 3.9+ installed
2. Dependencies: `pip install python-osc fastmcp`
3. Ports 8000-8001 not in use
4. Run with `python server.py`
5. Check console for errors

### Problem: Commands sent but no response

**Debug**:
```python
# Test OSC connection
from pythonosc import udp_client
client = udp_client.SimpleUDPClient("127.0.0.1", 8000)
client.send_message("/play", [])

# Should start playback if working
```

## Emergency Procedures

### If Reaper Crashes During Session

1. **Don't panic** - Reaper auto-saves
2. Reopen Reaper
3. File → Recent Projects → Recover
4. Check Audio/ folder for recorded files (even if project corrupted)

### If Recording Lost

1. Check Audio/ folder in project directory
2. Files are .wav format, named with date/time
3. Import files manually if needed
4. Reaper keeps recording even if crashed mid-session

## Getting Help

**In Order**:
1. This troubleshooting guide
2. Reaper-MCP documentation (README.md, docs/)
3. Reaper forums
4. Reaper support
5. GitHub Issues (for MCP-specific problems)

**When Reporting**:
- Reaper version
- Reaper-MCP version
- OS and audio interface
- Error messages (exact text)
- Steps to reproduce

---

## Prevention

**Daily**:
- Save frequently (Ctrl+S)
- Test OSC connection before session
- Verify audio routing

**Weekly**:
- Backup projects
- Update Reaper
- Clean temp files

**Before Important Sessions**:
- Test all equipment 1 hour early
- Have backup computer ready
- Verify all connections
- Create new project (don't reuse old)

---

**Austrian Reliability**: Prepare well, prevent problems, solve issues systematically! 🇦🇹

