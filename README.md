# OpenSpace
An audio spatialization system for headphones

Demos can be found in the demos folder

Usage: `$ openspace.py measures.json layout.json music.format`  
Edit measures.json and layout.json in config folder  
Place music file (any ffmpeg compatible format) in audio folder

### Requirements
- [Spleeter](https://github.com/deezer/spleeter)
- [ffmpeg](https://ffmpeg.org/)
- [PyOpenAL-HRTF](https://github.com/mmxgn/PyOpenAL-HRTF)
- The latest [OpenAL-Soft](https://openal-soft.org/) binary (replace binary from PyOpenAL-HRTF in Python environment)
  - Add hrtfs folder to OpenAL-Soft HRTF definition paths in config file
