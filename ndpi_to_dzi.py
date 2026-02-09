from pathlib import Path

import click
import pyvips

DEPTH_CHOICES = click.Choice(["onetile", "onepixel", "one"], case_sensitive=False)


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
        image = pyvips.Image.new_from_file(input_ndpi)
    except pyvips.Error as exc:
        raise click.ClickException(f"Failed to open '{input_ndpi}': {exc}") from exc

    try:
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
@click.argument("input_ndpi", type=click.Path(exists=True))
@click.argument("output_dzi", type=click.Path())
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
    input_ndpi: str,
    output_dzi: str,
    tile_size: int,
    overlap: int,
    quality: int,
    depth: str,
) -> None:
    """Convert NDPI whole-slide images to DZI format.

    Uses pyvips (libvips) for fast, multi-threaded tile generation.

    \b
    INPUT_NDPI  Path to the input NDPI file.
    OUTPUT_DZI  Path/name for the output DZI (e.g. "output" → output.dzi + output_files/).
    """
    convert_ndpi_to_dzi(
        input_ndpi,
        output_dzi,
        tile_size=tile_size,
        overlap=overlap,
        quality=quality,
        depth=depth,
    )


if __name__ == "__main__":
    cli()