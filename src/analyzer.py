import allin1

def analyze_audio(file_path: str):
    """
    Analyzes audio for BPM, Key, Structure (Segments) and Chords using the allin1 library.
    Returns a dictionary mapping chords to structure segments.
    """
    # allin1.analyze returns an Analysis object containing beats, downbeats, tempo, key, chords, and segments.
    result = allin1.analyze(file_path)
    
    # Get BPM and Key
    bpm_value = result.bpm
    key = result.key
    
    # Extract segments and map chords to them
    segments = []
    
    # result.segments is a list of Segment objects (start, end, label)
    # result.chords is a list of Chord objects (start, end, chord)
    
    for seg in result.segments:
        # Find chords that fall within this segment
        segment_chords = []
        for chord in result.chords:
            # We consider a chord part of the segment if its midpoint is within the segment
            chord_mid = (chord.start + chord.end) / 2.0
            if seg.start <= chord_mid < seg.end:
                # Add chord label (e.g., 'C:maj', 'A:min', 'N' for none)
                # Ignore 'N' chords (no chord)
                if chord.chord != 'N':
                    # Compress consecutive identical chords
                    if not segment_chords or chord.chord != segment_chords[-1]:
                        segment_chords.append(chord.chord)
        
        # Capitalize segment label (e.g., 'verse' -> 'Verse')
        label = seg.label.capitalize()
        
        segments.append({
            "name": label,
            "start_time": round(seg.start, 2),
            "end_time": round(seg.end, 2),
            "chords": segment_chords[:16] # limit to 16 chord changes to avoid huge payloads
        })
        
    # Prepare a flat list of chords for exact lyric alignment
    flat_chords = []
    for chord in result.chords:
        if chord.chord != 'N':
            # Only add if it's different from the previous one, or if it's the first
            if not flat_chords or flat_chords[-1]["chord"] != chord.chord:
                flat_chords.append({
                    "timestamp": round(chord.start, 2),
                    "chord": chord.chord.replace(':maj', '').replace(':min', 'm')
                })
                
    return {
        "bpm": round(bpm_value) if bpm_value else 120,
        "key": key if key else "Unknown",
        "segments": segments,
        "raw_chords": flat_chords
    }
