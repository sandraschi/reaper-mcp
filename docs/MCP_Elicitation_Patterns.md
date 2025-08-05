# MCP Elicitation Patterns - Interactive Tool Enhancement

**Date**: July 23, 2025  
**Context**: Sandra & Claudius MCP Server Factory 🇦🇹  
**Purpose**: Intelligent parameter elicitation for insufficient data scenarios  

---

## 🤔 **What is MCP Elicitation?**

**Elicitation** is the process of drawing out additional information when a tool call has insufficient parameters to complete its task effectively. Instead of failing immediately, the MCP server can intelligently request **precision** (clarification) from the user.

### **Traditional vs Elicitation-Enhanced Flow**

**Traditional (Fail Fast)**:

```
User: "Mute track"
MCP: Error - track_id parameter required
```

**Elicitation-Enhanced**:

```
User: "Mute track"
MCP: Which track would you like to mute?
     Available: 1(Drums), 2(Bass), 3(Guitar), 4(Vocals)
User: "The guitar track"
MCP: ✅ Muted track 3 (Guitar)
```

---

## 🎯 **Implementation Patterns**

### **1. Elicitation Response Structure**

```python
@mcp.tool()
async def mute_track(track_id: Optional[int] = None) -> Dict[str, Any]:
    """Mute a track with intelligent elicitation"""
    
    if track_id is None:
        # Return elicitation request instead of error
        tracks = await get_tracks()
        return {
            "_elicitation": True,
            "_request_type": "selection",
            "_parameter": "track_id",
            "_prompt": "Which track would you like to mute?",
            "_options": [
                {"value": t["id"], "label": f"{t['id']} ({t['name']})"} 
                for t in tracks
            ],
            "_example": "You can say: 'track 3' or 'the guitar track'"
        }
    
    # Normal execution with provided track_id
    return await perform_track_mute(track_id)
```

### **2. Elicitation Types**

**Selection Elicitation** (Choose from options):

```python
{
    "_elicitation": True,
    "_request_type": "selection",
    "_parameter": "format",
    "_prompt": "What output format do you want?",
    "_options": [
        {"value": "wav", "label": "WAV (Uncompressed)"},
        {"value": "mp3", "label": "MP3 (Compressed)"},
        {"value": "flac", "label": "FLAC (Lossless)"}
    ]
}
```

**Range Elicitation** (Numeric input):

```python
{
    "_elicitation": True,
    "_request_type": "range",
    "_parameter": "volume",
    "_prompt": "What volume level? (0.0 = silent, 1.0 = maximum)",
    "_min": 0.0,
    "_max": 1.0,
    "_current": 0.75,
    "_unit": "linear"
}
```

**Text Elicitation** (Free text input):

```python
{
    "_elicitation": True,
    "_request_type": "text",
    "_parameter": "marker_name",
    "_prompt": "What should this marker be called?",
    "_suggestions": ["Verse", "Chorus", "Bridge", "Solo"],
    "_example": "e.g., 'Guitar Solo Start'"
}
```

**Confirmation Elicitation** (Yes/No decision):

```python
{
    "_elicitation": True,
    "_request_type": "confirmation",
    "_action": "delete_all_tracks",
    "_prompt": "This will permanently delete ALL tracks. Are you sure?",
    "_warning": "This action cannot be undone!",
    "_default": False
}
```

---

## 🎛️ **Audio-Specific Elicitation Examples**

### **Reaper MCP Elicitation Scenarios**

**1. Ambiguous Track Reference**:

```python
# User: "solo the bass"
# Multiple bass tracks exist
{
    "_elicitation": True,
    "_request_type": "selection", 
    "_parameter": "track_id",
    "_prompt": "Multiple bass tracks found. Which one?",
    "_options": [
        {"value": 5, "label": "5 (Bass Guitar)"},
        {"value": 7, "label": "7 (Bass Synth)"},
        {"value": 12, "label": "12 (Sub Bass)"}
    ],
    "_context": "Currently working on: Project_Demo_v3.rpp"
}
```

**2. Incomplete Render Settings**:

```python
# User: "render the project"
# Missing format and quality settings
{
    "_elicitation": True,
    "_request_type": "multi_parameter",
    "_parameters": {
        "format": {
            "prompt": "Output format?",
            "options": ["wav", "mp3", "flac"],
            "default": "wav"
        },
        "quality": {
            "prompt": "Quality setting?", 
            "options": ["high", "medium", "low"],
            "default": "high"
        },
        "bounds": {
            "prompt": "What to render?",
            "options": ["project", "selection", "time_selection"],
            "default": "project"
        }
    },
    "_summary": "Render project with these settings:",
    "_austrian_efficiency": "Schnell und präzise! 🇦🇹"
}
```

**3. Time Position Clarification**:

```python
# User: "add marker at the good part"
# Vague position reference
{
    "_elicitation": True,
    "_request_type": "time_position",
    "_parameter": "position",
    "_prompt": "Where should I add the marker?",
    "_current_position": "2:45.230",
    "_suggestions": [
        {"label": "Current position (2:45)", "value": "2:45"},
        {"label": "Start of project", "value": "0:00"},
        {"label": "Custom time...", "value": "_custom"}
    ],
    "_input_formats": ["MM:SS", "MM:SS.mmm", "seconds"]
}
```

---

## 📱 **How Elicitation Shows in Claude Desktop**

### **Potential UI Implementations**

**1. Inline Follow-up** (Most likely current behavior):

```
Claude: I need more information to mute the track.
        Which track would you like to mute?
        Available tracks:
        • 1 (Drums)  
        • 2 (Bass)
        • 3 (Guitar)
        • 4 (Vocals)
        
        You can say "track 3" or "the guitar track"
```

**2. Interactive Selection** (Possible future):

```
Claude: [Track Selection Interface]
        ○ Track 1 (Drums)
        ○ Track 2 (Bass)  
        ○ Track 3 (Guitar) ← [selected]
        ○ Track 4 (Vocals)
        
        [Mute Selected Track]
```

**3. Smart Parsing** (Most elegant):

```
User: "mute the guitar"
Claude: [Automatically identifies Track 3 = Guitar]
        ✅ Muted track 3 (Guitar)
```

---

## 🔧 **Implementation in FastMCP 2.1**

### **Elicitation Middleware Pattern**

```python
def elicitation_tool(require_params: List[str] = None):
    """Decorator for tools that support elicitation"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check for missing required parameters
            missing = []
            for param in require_params or []:
                if kwargs.get(param) is None:
                    missing.append(param)
            
            if missing:
                # Generate elicitation response
                return await generate_elicitation(func, missing, **kwargs)
            
            # Normal execution
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@elicitation_tool(require_params=['track_id'])
async def mute_track(track_id: Optional[int] = None) -> Dict[str, Any]:
    """Mute track with intelligent parameter elicitation"""
    # This will auto-elicit track_id if not provided
    client = await get_reaper_client()
    return await client.set_track_mute(track_id, True)
```

### **Smart Context Inference**

```python
async def infer_missing_params(func_name: str, **provided_kwargs):
    """Attempt to infer missing parameters from context"""
    
    if func_name == "mute_track" and "track_id" not in provided_kwargs:
        # Try to infer from track names or current selection
        tracks = await get_tracks()
        
        # Check for natural language hints in conversation context
        recent_messages = get_conversation_context()
        for msg in recent_messages:
            if "guitar" in msg.lower():
                guitar_tracks = [t for t in tracks if "guitar" in t["name"].lower()]
                if len(guitar_tracks) == 1:
                    return {"track_id": guitar_tracks[0]["id"]}
        
        # Fall back to elicitation
        return create_track_selection_elicitation(tracks)
```

---

## 🎵 **Audio-Specific Elicitation Benefits**

### **1. Natural Language Processing**

- "Mute the drum track" → Auto-identify drum track
- "Turn up the vocals" → Find vocal tracks, elicit amount
- "Add reverb" → Elicit track, plugin type, amount

### **2. Context Awareness**

- Recently accessed tracks get priority
- Current transport position suggests marker placement
- Project genre influences effect suggestions

### **3. Austrian Efficiency**

- Reduce back-and-forth conversations
- Intelligent defaults based on context
- Professional workflow preservation

---

## 🚀 **Future Elicitation Enhancements**

### **1. Multi-Modal Elicitation**

- Visual waveform position selection
- Audio preview during parameter adjustment
- Real-time feedback during elicitation

### **2. Learning Patterns**

- Remember user preferences per project
- Suggest based on previous similar actions
- Adapt elicitation complexity to user expertise

### **3. Batch Elicitation**

- Collect multiple missing parameters in one interaction
- Preview complete action before execution
- Undo/modify elicited actions

---

## 💡 **Best Practices for MCP Elicitation**

1. **Fail gracefully**: Always provide helpful elicitation, never just error
2. **Context matters**: Use current state to inform elicitation options
3. **Austrian precision**: Be specific and clear in requests
4. **Efficiency first**: Minimize interaction overhead
5. **Learn and adapt**: Remember user patterns and preferences

---

*Austrian MCP Engineering - "Präzision durch Interaktion" 🇦🇹*
