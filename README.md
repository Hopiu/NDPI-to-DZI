# NDPI to DZI

Fast converter for NDPI whole-slide images to [DZI (Deep Zoom Image)](https://en.wikipedia.org/wiki/Deep_Zoom) format, powered by [libvips](https://www.libvips.org/).

## Features

- **Fast** — uses libvips for multi-threaded, streaming tile generation
- **Configurable** — tile size, overlap, JPEG quality, and pyramid depth as CLI options
- **Simple** — single command, sensible defaults matching the DeepZoom standard

## Prerequisites

- **libvips** with OpenSlide support (for NDPI reading)
  - Debian/Ubuntu: `sudo apt install libvips-dev`
  - macOS: `brew install vips`
  - Arch: `sudo pacman -S libvips`
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — Python package & project manager

## Installation

```bash
git clone https://github.com/<your-username>/NDPI2DZI.git
cd NDPI2DZI
uv sync
```

## Usage

```bash
uv run ndpi2dzi INPUT_NDPI OUTPUT_DZI
```

**Example:**

```bash
uv run ndpi2dzi slide.ndpi slide_output
```

This creates:

```
slide_output.dzi           # DZI XML metadata
slide_output_files/        # Tile directory
  0/0_0.jpeg               # Lowest-resolution level
  1/0_0.jpeg, 1_0.jpeg...
  ...
  N/...                    # Highest-resolution level
```

### Options

| Flag | Default | Description |
| --- | --- | --- |
| `--tile-size` | `254` | Tile size in pixels |
| `--overlap` | `1` | Tile overlap in pixels |
| `-q`, `--quality` | `90` | JPEG quality (1–100) |
| `--depth` | `onetile` | Pyramid depth: `onetile`, `onepixel`, or `one` |

**Example with options:**

```bash
uv run ndpi2dzi slide.ndpi output --tile-size 512 --overlap 2 -q 85 --depth onepixel
```

Run `uv run ndpi2dzi --help` for full usage info.

## License

[MIT](LICENSE)
