def align_chords_with_lyrics(chords: list, lyrics: list) -> str:
    """
    chords: List of dicts [{'timestamp': 0.0, 'chord': 'E'}, {'timestamp': 2.5, 'chord': 'Fmaj7'}]
    lyrics: List of dicts [{'start_time': 1.2, 'text': 'I drifted through the black light'}]
    """
    combined_output = []
    
    for line in lyrics:
        line_start = line.get('start_time', 0.0)
        
        # Find the most recent chord that happened before or at this lyric start
        current_chord = "N.C." # No Chord
        for c in chords:
            if c.get('timestamp', 0.0) <= line_start:
                current_chord = c.get('chord', 'N.C.')
            else:
                break
        
        # Format for Suno: [Chord] Lyric text
        if current_chord != "N.C.":
            combined_output.append(f"[{current_chord}] {line.get('text', '')}")
        else:
            combined_output.append(line.get('text', ''))
            
    return "\n".join(combined_output)

def generate_suno_prompt(bpm: float, key: str, chords: list, raw_chords: list, lyrics: list) -> str:
    """
    The LLM logic to turn data into a Suno prompt.
    Takes BPM, Key, List of Chords (segments), raw list of timestamped chords, and Timestamped Lyrics.
    """
    prompt = f"[Tempo: {bpm:.0f} BPM]\n"
    prompt += f"[Key: {key}]\n\n"
    
    # Simple heuristic for "Arrangement" based on the number of unique chords detected overall
    all_chords = set()
    for seg in chords:
        all_chords.update(seg.get("chords", []))
    
    if len(all_chords) > 6:
        arrangement = "lush and atmospheric"
    elif len(all_chords) > 0 and len(all_chords) <= 3:
        arrangement = "stark and empty"
    else:
        arrangement = "balanced and rhythmic"
        
    prompt += f"Arrangement: {arrangement}\n\n"
    
    for segment in chords:
        seg_name = segment.get("name", "Verse")
        start_time = segment.get("start_time", 0.0)
        end_time = segment.get("end_time", 999.0)
        
        prompt += f"[{seg_name}]\n"
        
        # Find lyrics for this segment
        segment_lyrics = []
        for lyr in lyrics:
            l_start = lyr.get("start_time", 0.0)
            l_end = lyr.get("end_time", 0.0)
            l_mid = (l_start + l_end) / 2.0
            
            if start_time <= l_mid < end_time:
                segment_lyrics.append(lyr)
                
        if segment_lyrics:
            # Align the exact chords inline with the segment lyrics
            aligned_text = align_chords_with_lyrics(raw_chords, segment_lyrics)
            prompt += aligned_text + "\n\n"
        else:
            prompt += "[Instrumental]\n\n"
            
    return prompt.strip()
