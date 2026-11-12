# Cutest picture

Entry for make.fun `cutest-picture-01`: a program that writes one picture —
the cutest picture — to `/output/entry.png`.

The picture is a fluffy baby kitten: huge amber eyes, a tiny pink nose, a
slight head tilt, on a soft pastel background. The program validates the
image (PNG or JPEG, at most 1 MiB and 1024×1024) and copies it byte-for-byte
to the output directory, so both runs write exactly the same bytes.

Run it locally:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
