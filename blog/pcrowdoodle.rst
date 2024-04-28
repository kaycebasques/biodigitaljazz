.. _pcrowdoodle:

=============================================
pCrowDoodle, my "desirable difficulty" laptop
=============================================

*2024 Apr 27*

.. _god of electronics: https://www.atlasobscura.com/places/dendengu

Next week Gabi and I head off to Japan for a 3-week vacation. The
`god of electronics`_ has blessed me with the motivation to tinker
during my flights. I'm in a bit of a pickle, though... what laptop
should I bring?

* I don't want to bring my work laptop. It's too big and I want to practice
  some "healthy detachment" from work.
* I don't have a lightweight personal laptop that's enjoyable to goof around
  on.

The solution for me, an irrational simpleton, was to spend too much money
on a highly questionable Raspberry Pi "laptop".

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi4.jpg

.. _CrowPi-L: https://web.archive.org/web/20240426205124/https://www.elecrow.com/crowpi-l-real-raspberry-pi-laptop-for-learning-programming-and-hardware.html

The official name of this product is `CrowPi-L`_ but mine only answers to the
moniker of *pCrowDoodle my beloved*.

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/gif/pcrowdoodle.gif

--------
"laptop"
--------

.. _Armadillo\: Opossum Heavy Armor: https://web.archive.org/web/20240426210415/https://timandraka.bigcartel.com/product/heavy-armor

pCrowDoodle is best thought of as the computer-equivalent of
`Armadillo: Opossum Heavy Armor`_:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/armadillo.jpg

You just lift the magnetically (??) attached back cover...

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi7.jpg

...and cram your RPi into the corner...

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi10.jpg

...and you're basically ready to fire pCrowDoodle up and realize that there's
some boot firmware that is impossible to update at best and backdoor'd at worst:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi5.jpg

---------------------
Form factor: wedgebot
---------------------

Cramming the RPi into the back results in a slope steep enough to downhill
race on:

.. raw:: html

   <video style="width: 100%; height: auto; object-fit: cover;" controls>
     <source type="video/mp4"
         src="https://raw.githubusercontent.com/kaycebasques/media/main/mp4/crowpi1.mp4"/>
   </video>

.. _Wheely Big Cheese: https://robotwars.fandom.com/wiki/Wheely_Big_Cheese

`Wheely Big Cheese`_ is dead, long live Wheely Big Cheese!

-------------------------------------
"Dual boot": quite pleasant, actually
-------------------------------------

pCrowDoodle came with a little SD expansion thingy that lets you switch
between an "A" SD card and a "B" SD card fairly quickly:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi8.jpg

I'm tempted to flip it while my RPi is running just to learn how much or little
damage that does...

RPi OS booted up pretty much without a hitch:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi6.jpg

And I even got OpenBSD working on the other SD!

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi9.jpg

Pretty excited about that. I'm going to leave it as a purely console-based
experience.

-----------------------------------------
Unusable trackpad: a blessing in disguise
-----------------------------------------

The trackpad is comically small and has already started to freeze up on me:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi3.jpg

But going into the purchase I expected the trackpad to be unusable. I
was kinda hoping for it, actually... I've been meaning to get really solid
at keyboard-based navigation. This is the main "desirable difficulty" thing
for me. The other cool thing is it's forcing me to find CLI commands for
common tasks such as locking the screen.

`Lobsters <https://lobste.rs>`_ on ``lynx`` somehow looks better than the
actual website??

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi11.jpg

------------------
40-pin GPIO header
------------------

You need a connector (which was annoyingly not included with my purchase)
but it's still possible to access all the pins:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi2.jpg

-------
Battery
-------

I got 3-5 hours on the first full charge. I fully expect this to drop down
to 30 minutes after a month. My coworker had the good idea of using a
cellphone power bank as a backup.

An interesting challenge (maybe project?) is that the RPi OS UI doesn't
seem to expect to run off battery so there's no "low battery" indicator.
Meaning when the battery's done pCrowDoodle just abruptly shuts down on me.
