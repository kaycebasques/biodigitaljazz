The special hell called "setting up the RPi camera module"
==========================================================

*2023 Nov 22*

It's actually super reasonable, *once you find the correct official docs*. But
good lord, did I learn this the hard way.

Long story short, don't trust any of the community content; rely solely on the
official RPi docs. And make sure that the doc you're reading was written for the
specific HW/SW permutation that you're using. In my case (RPi4 + RPi OS
Bookworm + RPi Camera Module 3) the correct doc is `The Picamera2 Library`_.

I'll leave you with this gem of a `quote`_ from an RPI engineer about the
situation.

    Hi, yes it's a bit of a minefield out there on the web because so much
    content is still referring to the legacy camera stack which will never
    (for example) support the camera module 3, or even work at all on any
    reasonably modern Raspberry Pi OS image.

.. _The Picamera2 Library: https://web.archive.org/web/20231110055853/https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

.. _quote: https://forums.raspberrypi.com/viewtopic.php?p=2077132&sid=bf88c686e19e24a18dc2a65ff932e437#p2077132
