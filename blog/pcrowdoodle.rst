.. _pcrowdoodle:

=============================================
pcrowDoodle, my "desirable difficulty" laptop
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

The solution for me, an irrational simpleton, was to spend perhaps too much
money ($200) on a questionable Raspberry Pi "laptop".

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi4.jpg

.. _CrowPi-L: https://web.archive.org/web/20240426205124/https://www.elecrow.com/crowpi-l-real-raspberry-pi-laptop-for-learning-programming-and-hardware.html

The official name of this product is `CrowPi-L`_ but mine only answers to the
moniker of *pcrowDoodle my beloved*.

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/gif/pcrowdoodle.gif

(This is not an "affiliate shill" post; I have nothing to disclose.)

--------
"laptop"
--------

.. _Armadillo\: Opossum Heavy Armor: https://web.archive.org/web/20240426210415/https://timandraka.bigcartel.com/product/heavy-armor

pcrowDoodle is best thought of as the computer-equivalent of
`Armadillo: Opossum Heavy Armor`_:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/armadillo.jpg

You just lift the magnetically (??) attached back cover...

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi7.jpg

...and cram your RPi into the corner...

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi10.jpg

...and you're basically ready to fire pcrowDoodle up and realize that there's
some boot firmware that's impossible to update at best and backdoor'd at worst:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi5.jpg

I'm using RPi 4. I have a hunch RPi5 won't work.

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

pcrowDoodle came with a little SD expansion thingy that lets you switch
between an "A" SD card and a "B" SD card fairly quickly:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi8.jpg

RPi OS booted up pretty much without a hitch:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi6.jpg

And I even got OpenBSD working on the other SD!

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi9.jpg

Pretty excited to finally try out BSD. Gonna leave it GUI-free.

-----------------------------------------
Unusable trackpad: a blessing in disguise
-----------------------------------------

The trackpad is comically small and has already started to freeze up on me:

.. image:: https://raw.githubusercontent.com/kaycebasques/media/main/jpg/crowpi3.jpg

Going into the purchase I expected this. I was kinda hoping for it,
actually... I've been meaning to get really solid at keyboard-based
navigation. This is the main "desirable difficulty" thing for me.
A cool side-effect of forcing myself to get good at keyboard-based
navigation is that I'm also learning the CLI-equivalent for common actions,
such as ``dm-tool lock`` to lock the screen.

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
to 30 minutes after a month.

An interesting challenge (maybe project?) is that the RPi OS UI doesn't
seem to expect to run off battery so there's no "low battery" indicator.
So when the battery's done pcrowDoodle abruptly shuts down on me. Maybe
there's just some bit in ``raspi-config`` I need to flip.

My coworker, Rob, had the interesting idea to supplement the battery reserves
with a cellphone power bank. The power bank would probably have some
"low charge" indicator, too.

-----------------------------------
Where have all the RPi laptops gone
-----------------------------------

I've poked fun at Elecrow (the maker of the CrowPi-L) a few times but
it seems like they deserve my thanks and respect: "RPi laptop" is a
cool idea and they seem to be one of only a handful of companies actually
making it happen.'

RPi OS is a sweet spot for exploratory hacking IMO:

* It's trivial to set up on an SD card
* It comes pre-loaded with lots of interesting stuff
  (``for name in $(ls /usr/bin); do man -f $name; done``)
* It's the same ecosystem of tools/programs/etc. as my work env
  <3 Debian
* The RPi hardware itself really invites you to learn about it
  on a deeper level. Have you seen those datasheets? Delightful

---------
Worth it?
---------

Too soon to tell. I'll report back after Japan. It will boil down to
reliability; if this thing starts crashing or the keys start sticking then
I'm screwed.

At first I thought $200 was too expensive but realistically, it would cost
me much more than $200 in time/energy/parts/hairline to try to build something
like this myself.
