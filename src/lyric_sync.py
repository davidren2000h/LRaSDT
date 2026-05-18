"""
lyric_sync.py - Match current playback time to the correct lyric line.
"""


def get_current_lyric_index(current_time, lyrics):
    """
    Given current playback time, return the index of the lyric line
    that should be displayed.

    Args:
        current_time: current playback position in seconds
        lyrics: list of dicts with 'start', 'end', 'text' keys

    Returns:
        int: index of the current lyric, or -1 if no lyric matches
    """
    if not lyrics:
        return -1

    # Before first lyric
    if current_time < lyrics[0]["start"]:
        return -1

    # Find the matching lyric
    for i, seg in enumerate(lyrics):
        if seg["start"] <= current_time <= seg["end"]:
            return i

    # Between lyrics (in a gap) — show the previous lyric
    for i in range(len(lyrics) - 1):
        if lyrics[i]["end"] < current_time < lyrics[i + 1]["start"]:
            return i

    # After all lyrics
    if current_time > lyrics[-1]["end"]:
        return len(lyrics) - 1

    return -1


def get_display_lines(current_time, lyrics):
    """
    Return previous, current, and next lyric lines for display.

    Args:
        current_time: current playback position in seconds
        lyrics: list of dicts with 'start', 'end', 'text' keys

    Returns:
        dict with 'previous', 'current', 'next' text strings
    """
    idx = get_current_lyric_index(current_time, lyrics)

    result = {
        "previous": "",
        "current": "",
        "next": "",
        "index": idx
    }

    if idx < 0:
        # Before first lyric — show first as next
        if lyrics:
            result["next"] = lyrics[0]["text"]
        return result

    if idx > 0:
        result["previous"] = lyrics[idx - 1]["text"]

    result["current"] = lyrics[idx]["text"]

    if idx < len(lyrics) - 1:
        result["next"] = lyrics[idx + 1]["text"]

    return result
