# Image Assets

This directory contains the image assets used by the Davidic Lyre app.

## Expected Files

| File                | Purpose                                      |
|---------------------|----------------------------------------------|
| `icon.png`          | App launcher icon (512×512 px recommended)   |
| `presplash.png`     | Splash screen shown at startup               |
| `wood_texture.png`  | Wood grain texture for the lyre body         |

## Specifications

- Format: PNG (with transparency where needed)
- Icon: 512×512 px minimum, square
- Presplash: match target device resolution (e.g., 1440×2176 for Fold5 inner screen)
- Wood texture: tileable, warm brown tones per the PRD color palette:
  - Light wood: `#A87442`
  - Medium wood: `#7A4E2A`
  - Dark wood: `#4A2E1A`
  - Highlight/wear: `#C99562`

Place all image files in this directory before building or running the app.
The `buildozer.spec` references `assets/images/icon.png` and `assets/images/presplash.png`
as the app icon and presplash screen.
