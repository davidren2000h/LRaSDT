# Bug Reports & Fixes

Report bugs below. Each bug will be reviewed and fixed. Once fixed, a summary is added here.

## Template

```
### [Bug Title]
- **File/Module**: Which file or module is affected
- **Steps to Reproduce**: How to trigger the bug
- **Expected Behavior**: What should happen
- **Actual Behavior**: What happens instead
```

## Bug List

### Bug #1: ERROR: expected language as parameter (GitHub Issue #1)
- **Reported by**: HongyiRen2009
- **File/Module**: `src/transcriber.py`, `src/app.py`
- **Steps to Reproduce**: Select an MP3 file, click "Load TXT & Align", select a TXT lyrics file
- **Actual Behavior**: Error: "expected language as parameter"
- **Root Cause**: `stable_whisper`'s `model.align()` requires a `language` parameter, but it was not being passed
- **Fix**: Added `language` parameter to `align_lyrics()` in `transcriber.py` (defaults to `"en"`), and added a Language dropdown (en/zh/ja/ko/es/fr/de) to the GUI in `app.py`
- **Status**: Fixed — commit `a67a270`
