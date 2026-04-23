from pathlib import Path
from typing import Any, cast

import click
import pyvips

DEPTH_CHOICES = click.Choice(["onetile", "onepixel", "one"], case_sensitive=False)


def find_ndpi_files(input_dir: Path) -> list[Path]:
    """Return NDPI files in a directory (case-insensitive), sorted by name."""
    return sorted(
        [path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() == ".ndpi"]
    )


def convert_ndpi_to_dzi(
    input_ndpi: str,
    output_dzi: str,
    *,
    tile_size: int = 254,
    overlap: int = 1,
    quality: int = 90,
    depth: str = "onetile",
) -> None:
    """Convert an NDPI file to DZI format using pyvips."""
    # Strip .dzi extension if provided — dzsave appends it automatically
    output = str(Path(output_dzi).with_suffix(""))

    try:
        image = cast(Any, pyvips.Image.new_from_file(input_ndpi))
    except pyvips.Error as exc:
        raise click.ClickException(f"Failed to open '{input_ndpi}': {exc}") from exc

    image.set_progress(True)

    try:
        with click.progressbar(length=100, label="Converting") as bar:
            last_percent = [0]

            def eval_cb(_image, progress):
                delta = progress.percent - last_percent[0]
                if delta > 0:
                    bar.update(delta)
                    last_percent[0] = progress.percent

            image.signal_connect("eval", eval_cb)

            image.dzsave(
                output,
                suffix=f".jpeg[Q={quality}]",
                tile_size=tile_size,
                overlap=overlap,
                depth=depth,
            )
    except pyvips.Error as exc:
        raise click.ClickException(f"Failed to save DZI: {exc}") from exc

    click.echo(f"Conversion complete: {output}.dzi")


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.argument("output_path", type=click.Path(path_type=Path))
@click.option("--tile-size", default=254, show_default=True, help="Tile size in pixels.")
@click.option("--overlap", default=1, show_default=True, help="Tile overlap in pixels.")
@click.option("-q", "--quality", default=90, show_default=True, help="JPEG quality (1-100).")
@click.option(
    "--depth",
    default="onetile",
    show_default=True,
    type=DEPTH_CHOICES,
    help="Pyramid depth: onetile, onepixel, or one.",
)
def cli(
    input_path: Path,
    output_path: Path,
    tile_size: int,
    overlap: int,
    quality: int,
    depth: str,
) -> None:
    """Convert NDPI whole-slide images to DZI format.

    Uses pyvips (libvips) for fast, multi-threaded tile generation.

    \b
    INPUT_PATH  Path to an NDPI file or directory containing NDPI files.
    OUTPUT_PATH For a file input: path/name for the output DZI
                (e.g. "output" → output.dzi + output_files/).
                For a directory input: output directory where each NDPI is converted
                using its stem name (e.g. scan.ndpi -> OUTPUT_PATH/scan.dzi + scan_files/).
    """
    if input_path.is_file():
        convert_ndpi_to_dzi(
            str(input_path),
            str(output_path),
            tile_size=tile_size,
            overlap=overlap,
            quality=quality,
            depth=depth,
        )
        return

    if not input_path.is_dir():
        raise click.ClickException(f"Input path is neither a file nor directory: {input_path}")

    if output_path.exists() and output_path.is_file():
        raise click.ClickException(
            f"Output path must be a directory when input is a directory: {output_path}"
        )

    output_path.mkdir(parents=True, exist_ok=True)

    ndpi_files = find_ndpi_files(input_path)
    if not ndpi_files:
        raise click.ClickException(f"No .ndpi files found in directory: {input_path}")

    click.echo(f"Found {len(ndpi_files)} NDPI file(s) in {input_path}")

    for ndpi_file in ndpi_files:
        click.echo(f"\n[{ndpi_file.name}]")
        target = output_path / ndpi_file.stem
        convert_ndpi_to_dzi(
            str(ndpi_file),
            str(target),
            tile_size=tile_size,
            overlap=overlap,
            quality=quality,
            depth=depth,
        )


if __name__ == "__main__":
    cli()