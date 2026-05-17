# CowAgent Theme Generator

Generates day/night themes from wallpaper images for the CowAgent web interface.

## Features

- **Color Extraction** - automatically extracts dominant colors from wallpapers using image analysis
- **Day/Night Mode** - generates two matching color schemes for light and dark themes
- **Coordinated Design** - sidebar and chat area colors are automatically harmonized
- **One-Click Install** - installs to CowAgent with automatic backup of original files
- **Preview** - preview color combinations before installation

## Usage

### Option 1: Pre-built executable

1. Download `CowAgent-ThemeGenerator.exe` from Releases
2. Run the executable
3. Click "Select Wallpaper" to choose an image
4. Click "Generate Theme"
5. Click "Install to CowAgent"

### Option 2: Run from source

```bash
pip install -r requirements.txt
python theme_generator.py
```

### Option 3: Build executable

```bash
build_exe.bat
```

## How it works

1. **Image Analysis** - uses PIL to analyze color distribution in the wallpaper
2. **Color Extraction** - extracts dominant colors through color clustering algorithm
3. **Color Calculation** - generates light and dark color schemes from extracted colors
4. **Style Generation** - automatically creates CSS and HTML files
5. **Installation** - copies files to CowAgent directory with automatic backup

## File structure

```
cow-theme-generator/
├── theme_generator.py    # Main program
├── requirements.txt      # Python dependencies
├── build_exe.bat         # Build script
└── README.md            # Documentation
```

## Generated files

- `chat.html` - Main page HTML
- `custom-theme.css` - Custom styles
- `chat-bg.jpg` - Background image

## Notes

- Supported formats: PNG, JPG, JPEG, BMP, GIF
- HD wallpapers recommended for best results
- Original files are automatically backed up to `custom_backup/` directory

## License

MIT
