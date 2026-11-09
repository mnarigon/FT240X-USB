## An FT240X-based parallel to USB converter

===== Description =====

This is an FT240X-based parallel to USB converter intended as an option for John Monahan's S-100 bus computer boards.

NOTE: These are the prototype files and I have not yet built and tested the prototype. I plan to update these files when that is complete. Quantity 5 boards was roughly $12 with tax and two-week shipping. Parts for 5 boards was roughly $50 with tax and one week shipping.

===== Design Files =====

The design files are in KiCad 10. The board fabrication parameters are 1.6mm, 2-layer, with 1 oz copper. There is a BOM in the documents folder.

===== Assembly Steps =====

  - Tin all the solder pads with the appropriate amount of solder.
  - Mount the front and back passives.
  - Mount the 24-SSOP transceiver.
  - Replace pins 1 and 9 on each 9-pin SMD connector header with pins from the THT connector header.
  - Mount the connector headers.
  - Mount the mini-USB connector.

The FT240X requires programming to enable the PWREN# functionality. For use in John's boards this is not required since John's designs do not use PWREN# and by default the signal is tri-stated.
