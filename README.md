# Video2tiff - Video Frame Extractor

A Python tool for extracting specific video frames as high-quality TIFF images with millisecond precision.

## Features
- 🎥 Supports multiple video formats (MP4, AVI, MOV, MKV)
- ⏱️ Millisecond-accurate frame selection (hh:mm:ss.xxx format)
- 🌐 Multilingual interface (English/日本語/中文)
- 📁 Automatic directory management
- 🖼️ Lossless TIFF output format

## Installation
```bash
# Install requirements
pip install -r requirements.txt

# Create necessary directories
mkdir -p video img
```

## Usage
```bash
python extract_frame.py
```

### Workflow
1. Select interface language
2. Choose from available videos in `/video` folder
3. Input timestamp (e.g. 00:01:23.456)
4. Output TIFF saved to `/img` folder

## File Structure
```
avi2tiff/
├── video/          # Input videos
├── img/            # Output TIFF images
├── extract_frame.py  # Main script
├── languages.py    # Multilingual translations
└── requirements.txt # Dependencies
```

## Dependencies
- `opencv-python`: Video processing and frame extraction
- `Pillow`: TIFF image saving and format handling

## Supported Time Formats
| Format          | Example       | Description                 |
|-----------------|---------------|-----------------------------|
| hh:mm:ss       | 01:23:45      | Seconds precision           |
| hh:mm:ss.xxx   | 01:23:45.678  | Millisecond precision       |

## License
MIT License