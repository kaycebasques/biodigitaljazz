.. _picam:

The eleventh circle of hell: setting up an RPi camera module
============================================================

*2023 Nov 22*

Short story long, don't trust any of the community content; it's full of ghosts
and wolverines and those people you meet at parties that start the
conversation with "so what do you do?"... Rely solely on the official RPi
docs. And make sure that whatever you're reading was written for the
specific HW/SW permutation that you're using. In my case (RPi4 + RPi OS
Bookworm + RPi Camera Module 3) the correct doc is `The Picamera2 Library`_.

This gem of a `quote`_ from an RPi engineer sums up the situation:

    Hi, yes it's a bit of a minefield out there on the web because so much
    content is still referring to the legacy camera stack which will never
    (for example) support the camera module 3, or even work at all on any
    reasonably modern Raspberry Pi OS image.

I'm not writing this post to complain; who has time for that? This is just
a courtesy heads up to my fellow hackers.

.. raw:: html

   <p style="margin-top: 10000px;">
       Huh? You're still here? And you scrolled all the way down here just
       to ask "What's the tenth circle?" Excellent question. I have no idea.
   </p>

.. _The Picamera2 Library: https://web.archive.org/web/20231110055853/https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

.. _quote: https://forums.raspberrypi.com/viewtopic.php?p=2077132&sid=bf88c686e19e24a18dc2a65ff932e437#p2077132
