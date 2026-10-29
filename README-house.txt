House Book
==========

The face on these pages is a modified version of New Computer Modern 8.1.1, by
Antonis Tsolomitis, itself based on Donald Knuth's Computer Modern.

  House Book         from NewCM10-Book.otf

It is set inline in each page (index.html and 404.html), as a WOFF2 data URL, so
that each page is whole in itself.

The original
------------

New Computer Modern is distributed on CTAN at

  https://ctan.org/pkg/newcomputermodern

under the GNU General Public License version 3 or later with the font exception,
or the GUST Font License (the LaTeX Project Public License 1.3c, with a request
that derived works be renamed). This modified version is distributed under the
GUST Font License. The complete, unmodified original is always obtainable from the
address above.

What was changed
----------------

1. Subset to printable ASCII, and the en dash and right single quotation mark
   where a page uses them.
2. OpenType layout features kept: kern, liga, smcp, c2sc, onum, lnum, pnum, tnum.
   All others removed.
3. The FontForge metadata tables FFTM and PfEd removed.
4. Renamed, at the GUST Font License's request: family "House Book", PostScript
   name HouseBook-Regular. The name table's description field carries a short form
   of this notice.
5. Converted to WOFF2, and set in each page as a data URL.

It was made with the fontTools subsetter: first from the original file named above
to 280 characters, then from that to the characters of each page.

Support
-------

Neither Antonis Tsolomitis nor Donald Knuth, nor anyone else involved with the
original, provides any support for this modified version. Questions about it
belong here, not upstream.
