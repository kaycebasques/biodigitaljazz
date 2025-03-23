.. _favicon:

===================================
Generating random animated favicons
===================================

This blog post is a meandering exploration of a random idea I had while
walking: can I auto-generate a random favicon on every pageview?

---------
Prior art
---------

Don't know, don't care. I'm doing this for fun. I enjoy encountering new ideas
through the creative process.

-------------
Random colors
-------------

To begin, what if I just generate a random color in every pixel? What will that look like?

.. _Rocket: https://rocket.rs
.. _Render: https://render.com

In my first implementation, I generated the favicon server-side. You can see the full
code in :ref:`server` but I quickly realized that this approach wouldn't work. Or at least,
it was sub-optimal. More on that later.

It took awhile, but I eventually got the server-side implementation working and
was pretty excited to see the result:

.. raw:: html

   <img id="random_16x16" width="16" height="16"/>

   <script>
     (() => {
       const canvas = document.createElement('canvas');
       canvas.width = 16;
       canvas.height = 16;
       const ctx = canvas.getContext('2d');
       for (let y = 0; y < canvas.height; y++) {
         for (let x = 0; x < canvas.width; x++) {
           const r = Math.floor(Math.random() * 256);
           const g = Math.floor(Math.random() * 256);
           const b = Math.floor(Math.random() * 256);
           ctx.fillStyle = `rgb(${r},${g},${b})`;
           ctx.fillRect(x, y, 1, 1);
         }
       }
       const data = canvas.toDataURL('image/png');
       document.querySelector("#random_16x16").src = data;
     })();
   </script>

TV static! My grid of random colors (kinda) looks like TV static.
Obvious in hindsight, but I did not see that coming.

16x16 (the size of a basic favicon) is a little hard to see.
Here's 100x100:

.. raw:: html

   <img id="random_100x100" width="100" height="100"/>

   <script>
     (() => {
       const canvas = document.createElement('canvas');
       canvas.width = 100;
       canvas.height = 100;
       const ctx = canvas.getContext('2d');
       for (let y = 0; y < canvas.height; y++) {
         for (let x = 0; x < canvas.width; x++) {
           const r = Math.floor(Math.random() * 256);
           const g = Math.floor(Math.random() * 256);
           const b = Math.floor(Math.random() * 256);
           ctx.fillStyle = `rgb(${r},${g},${b})`;
           ctx.fillRect(x, y, 1, 1);
         }
       }
       const data = canvas.toDataURL('image/png');
       document.querySelector("#random_100x100").src = data;
     })();
   </script>

-----------------------------------------------
Tangential inquiry into the nature of TV static
-----------------------------------------------

What the heck is TV static, anyways? It was one of those things that
just existed in the subconscious of my 90s childhood. I wasn't curious
about technology back then.

Here's a brief description of 90s TV (and static) for my fellow hackers born in
the 2000s and later who have probably never experienced it. Back then, you
couldn't watch whatever you wanted, whenever you wanted. There was a fixed set
of channels, and they played content on a fixed schedule. If you wanted to
watch the new episode of The Simpsons, you had to tune in at 8PM on Sundays.
Other times, you'd just flip through the channels and find something to watch,
like this:

.. raw:: html

   <iframe src="https://www.youtube.com/embed/XuWInDErrTU"
           style="width: 100%; aspect-ratio: 560 / 315;"
           title="An example of TV static"
           frameborder="0"
           referrerpolicy="strict-origin-when-cross-origin"
           allowfullscreen></iframe>

Eventually, you'd hit a channel with no content on it, and see something
like this:

.. raw:: html

   <iframe src="https://www.youtube.com/embed/J_FVFMdiZ0w"
           style="width: 100%; aspect-ratio: 560 / 315;"
           title="An example of TV static"
           frameborder="0"
           referrerpolicy="strict-origin-when-cross-origin"
           allowfullscreen></iframe>

That's TV static. So what the heck is it?

It's easier if we start with channels. The mechanics are much closer to AM and
FM radio than I realized. To the TV, "putting on channel 2" meant tuning the
TV's video receiver to a specific frequency and the audio receiver to another
specific frequency and then outputting the data received at those specific
frequencies.

.. _cosmic microwave background: https://en.wikipedia.org/wiki/Cosmic_microwave_background

Now, static. The gist of the phenomenon is that old TVs were always outputting
whatever their audio and video receivers were picking up, and sometimes there
wasn't actually any meaningful data being broadcast over the particular channel
that the TV was receiving. The TV would therefore be outputting random
electromagnetic radiation (RER). Where did the RER come from? The TV itself
generated some. Other electronic devices generated some, too. And, coolest of
all, around 1% of it came from the `cosmic microwave background`_ of the Big
Bang!

Sources:

* `The evolution of television <https://socialsci.libretexts.org/Bookshelves/Communication/Journalism_and_Mass_Communication/Book%3A_Mass_Communication_Media_and_Culture/09%3A_Television/9.01%3A_The_Evolution_of_Television>`_

* `Noise (video) <https://en.wikipedia.org/wiki/Noise_(video)>`_

* `Why don't TVs have static and white noise anymore? <https://www.howtogeek.com/840090/why-dont-tvs-have-static-and-white-noise-anymore/>`_

* `Analog television <https://en.wikipedia.org/wiki/Analog_television>`_

While doing this research, I realized that TV static was often black and white.
Maybe I had an unusual TV that output static with color, or maybe my memory is
mistaken. I kinda remember that static looked black and white from afar, but if you
got up close, you saw colors. So maybe if I animate the static at a fast rate, use a
lot of pixels, and look at it from far away, it will look black and white…?

-----------------------
Animating the TV static
-----------------------

Once I realized that my random grid of colors looked like a frame of TV static,
my mission became to fully recreate the TV static experience by animating my favicon.
Is that even possible? You would think that browser vendors might not allow it,
because animated favicons could potentially be very distracting and annoying. Only
one way to find out!

At this point, I ditched the server-side implementation. I'll probably need tens
of frames of static every second. Going to the network for every frame would
generate a stupid amount of network traffic. I could probably figure out a way to
make the server-side implementation work, but this is just a silly project for fun
so I'm going to switch to the more obvious solution: client-side JavaScript.

The basic idea is to render the random colors into a canvas and then use a data URL
to convert that into an image:

.. code-block:: html

   <img id="random_16x16" width="16" height="16"/>

   <script>
     const canvas = document.createElement('canvas');
     canvas.width = 16;
     canvas.height = 16;
     const ctx = canvas.getContext('2d');
     for (let y = 0; y < canvas.height; y++) {
       for (let x = 0; x < canvas.width; x++) {
         const r = Math.floor(Math.random() * 256);
         const g = Math.floor(Math.random() * 256);
         const b = Math.floor(Math.random() * 256);
         ctx.fillStyle = `rgb(${r},${g},${b})`;
         ctx.fillRect(x, y, 1, 1);
       }
     }
     const data = canvas.toDataURL('image/png');
     document.querySelector("#random_16x16").src = data;
   </script>

I tried combining this with ``setInterval`` to generate a new frame
of static every millisecond but it wasn't fast enough. Also, my computer
fan started to sound like a jet engine revving up for takeoff, so I assume
it required a stupid amount of CPU time.

So I started to think about that humble yet fascinating feature of the
web platform known as data URLs. There's something magical about the fact
that I can render an image into a canvas and then convert that into a URL.
What do those data URLs look like? How do they work? Is there a way for me
to just manipulate data URLs directly to reduce compute cost?

---------------------------
Shallow dive into data URLs
---------------------------

Generating 10 images and logging out each data URL (and its length) yields
a few obvious patterns:

.. code-block:: text

   Image 0
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA71JREFUOE8FwQsw1wcAwPHvT5fX4cg/8rqjh2qVlUcJ2UZIdJOrJEWlRpdXS5Y/97deNslzJq9/+qsorC1W+3tUJjHFzE4eM8niDJuTPGqc3z4fwWdYT8z84xrTL0KQ5ExzfGkbVRJL3nzkSpn7ThqDRtgTas1fqb/g06eBYUMNX0/pYVorZUiZgFDkIIp+7VnUJyaw4P8Ot5cDDKeVUFWeym/eFzAOCOdHeRGHG+cwPv85joNG9Ev6cK7tpiVpDCFUri4elqnTW2FC4c1oVhs8pKU3mEOKxRgfc8HhZz9s4pfxoMKVNWXxRIX3E6aMReNpIe3jCoQE/UrR3M0Cmcu3jHQ0s8zgK/anaCLLecvRAm8sWtZz9bYhqsOmWG/PIlqUsTL0Nh57IzCfkiL0hQ2Je08XojwpZcLLmT9nsii2esZBa2sGlJ74xm7gdFASkZtiSG56Qet3Aby60knik3g8q20RND+LFLP91Un6MBXDoAZqpi7z8apu6ljg/P0oDC5kMOu1jxy1rURtqqDtfB13z9gQ2F9Jud0PCEdK9ojxS1LQz5BSZl9A5NFKjN7XcmvpdpJvPee6lRk3mxoxu6yJqvw2PTvskW0OYfaUBr0NUQjZ/ynEjQoD9oQNoqv7N4bGd7nx7BuGFtWhdsWCzRkJHE4NJnNmkkm9WloDE8mtkaGTnkqs7CpCz8iEKNVTYf3ZHEzriogsGMPWuwa7vuv4Dc/h211OSKAmJx7no70ij6yuaL7wMOWRljkTK7UQTMxMxDJ7K7R6wlG6B/Im+g5J1fXcCy0n5nU681U6pJmcQfsDfxJVmulZ4Ud4fCvV83n8WhqMULl7v5g23MFT8yBWaTxiwGeULpkbo1YObCkeJEG6hXU6D+goMaFFJ5+OJH+Scwd4vOEgcWt8EGKWXxJD9rsxHZqC7/N/mIqT02Y4yNKAeU6eG2L8vQrFTZtx1NjGqeMLTB1wRV7twj3vWXRnjiD4qTmJsrl6jr4KZjT6GBLFYpwmNQiNKkAZt5VdJgkovLJxblKjPrKd0sBO8tXruROTj7Q7AqEtJ0Y0eCvBVasUd1szXu4Mwr1glkD5Rc4Wb6Mmey3fb8mkttqDOJvleP7kwQx6jN+IxW0yF+HgoTLRSO8JXZbaZLlY0T/yKab/BmNa6UifvjfaTil8ObYI2hTYWr1m4uFdluy6RpWqO2qlqQgbF3mI7bvP0Vwv4cAnJyitsWNIspYd7pb8XpfHu95LXE6XkH4xi8594USUruPASimr76+hu2QZ/wPXxoi33ZJ2AAAAAABJRU5ErkJggg==

   Image 1
   Length: 1398
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA8BJREFUOE8FwQ801AcAwPHvT2TIxboKSbnNYZ69tReprP8kVqNeXguvFCq7nifeaZfIlT+lS6XyJ0RZtvNa7MbKn7ErjSt/0r+h5om2lLayXiH67fMRMqfPFfNWWFPb487pw+WMXc3kyrmVmM635vrWSI7qrEjIbCa7V8O3y5fS02uNc4yK8Q1a1IfKEEq6ksXGfdMpONyBYut9FpdquHxLjXamjizfcOxyXHHctBS3rAbO3PuHkIjrlDi2sD41h0WdbxBmDw6KN9+l4Vs5Qa59OqrIBOJrWvF/0otRhJwN73RMcUyl/YMaXGSNRFb00fq7nnjtcyImDSD0lHiJEyYdnP3bjdvy4yi8q3j5KpaMh/2MHAth3jQPtsjk9CunU2s3jFNIPj7JdphKwgnWfo+QbPSnGKxKZ+ahz+lS/4ptx1UWvLpG0JUwuuJ3YRG8kIEsLTXjz1AOy1nv4YH8pwpislowe7scoWadregZu45A793MVczggsUllPtG8XzyER+2pbBsdxmPV8Ti3S1lOCCOvG3hGNTr6Z70I06p/QjyX1zFHcs2Y1U3jp/DPQwbW6hMuozFrF4CpWbEmXdgWR2Au3Mi5sZu3DhiTenGDFauqMZMP4TgfzJR/HfqQ1xTC7jrkcQ5+43syE5EG36DmLEx/ILn8qzbCLOsOlr2F5P7TSSeKVNoMPkNK6thhCalIM5zKabqoAGDQobmi/lMOuWASWEo+hNGKE2LaC+Mp77pEo2lTnyq2c0SvT0DbTtY8JkVgrz9sbgzrYljTUr+cqhmoqsEIWoDPXoDOQHOuBScpTf1ZxyVg0gli7BNKeLUgD/Kr/oYuT0LYaAvTvzyj6NEd7cz40wF27yi0a/yZnazK01Lvsb8hsjaNRY0SnLxTztJqbSLvk57lljmoztug5AUkS+6P7TjuEaGx9M9TK0dZ079GHuHvEh6/5YojZLN/w1y7VYkijsTDPmGYmzry6YSZ84vj0U4sjpM3C4Rebqmkvs1ajL3r2aKSR6Wmu2o6ptxtIlDbAtHdiIIm0KB51JTMrIl+PTX0mL+CMHHqFx0Nzbm4JiOhoK3RKw1Q7KwmvfJN8l+4YPXgUHqOyzY8/IBZWGrOO9pSeAPBhJUhbSGpSMo7zwWH0ku0lg5h/gtRxgOiSL09giZPjuRFl/g9ZsqVoaWM1lxgJHEBLY7f8xdgwXfySSUlzxAsBlNEV0uFqHzGsUgnuB5ewKb3/vhUGdL9Iun7G0dYbK6mU+mXWHX6VBeu3WyWPWaa9VBpMSI/A//Got8Xdx8PgAAAABJRU5ErkJggg==

   Image 2
   Length: 1386
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA7lJREFUOE8FwQs01XcAwPHvL2Nn5eycXBUpNamGFFa5O6eJbYbUNFt5dHvMI+Jo1jw6ukKspLW8E1bucvIK3cQ2wnpOHseccuXRKkOO1NXGbsXpv89HPNdqpbr0NPxqWknwn0PZ1lwcg7Zz/kUUGTZ65HtIxKnjGW+w42LVbnKt7rI5qot12SfpVpUidu2oliadJpic64DjOhkHTy3mO8s4bDRD6JsbYdtZiudOe1anz6DUHCM5MI2YeF+u93VRsdcL4UyzVLP0ChWaDJ47uGHfdh9byY00kwS8zP7mjvUuEu4+5vTUOaIC79Ht8gFDsbspfT+cPdNmiKSIa5J4q5yAL9sYq/uGbz+spMZ1EnHoOA9Uh9E0raL+9Q50vdEcXBRNXugSbFRqtroo+cLya4Suc0Y6236Fbc456Cd+RvSPVTx8+ZiZB1pE8m/0Flmhf1UP5Xw9WibCWWCVxxqlmrLxIgLXGyP2X1BIIz8Hk7NwLtr8HWz7YYybEx6cMi3ljXkyhmdvccAxmFf5MRwa1jFy1JvewH6mnjiw4m4mwvbRCkk2eI75xSGIRVtof3kHd3UZzs+dGBwO5G2VAzvjdHikhnFEbseshneZWWVIvFUV5dF9iE8b9kkF1z0oy+3ivwIb+psucyM/BoqS6E75k6+0GrYbzCagqZqcm67Irm3CzaeRhDV9HHCSEHNfeEvtTZFU5maQcaadX2ev5JOn1oxk+1E7NcBftQPsUXUgqx5ixiSDA+0SkTca2bh8jEstKxGxHx+WbArq6Ukd4POUNOQP27F4dI+E6XmkVU6TGeRMc2Uk3umT+GW1stzUjwldCfdCf8FO44soaZZL5tZrydRtpm2wg7jzC/E9acWSn7xwLGuh3309h+6PMzrLmquyThpNz9NnGURhhAV/fP8akTPvhHSJHsIdriBfEkpohB6nFUFMdjaS5JlKptIc7e/lrE82JVDhhevlcJ5WyNgwaYTwfonoG7gvTVvW4n4rHnHGBcOjZvSPNlASu4CAYAPs47JhnwPBVTpS3nPjqXYaaXEu9gmZ9OmWIYKUJ6RERTGG2f5cPL6J9LxhLG6v5cFHhfiMtVEsO0xxYTb+HbPwvCgISZJT8E8vda1DROzfgFCEGEnqOc/QpCeT5SunJ+Y284xriRvywbFmI7NfncKIZ5iuM2SLawt+9UnYGUeyRvEOEzkCcaFjmZSlCuPfAkeOvBnlQlgF8a3WiEI1zYm2GDwZwUTuyVKX1SgHu7FRq9i+t4XqKWf0Fan8D28sl88mkeyBAAAAAElFTkSuQmCC

   Image 3
   Length: 1390
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA7tJREFUOE8FwQ801AcAwPHvb1FvXm09TVZ5Wf5UnhGTtfKfs3Ki1Wpz4TRNKXYxQlx0aIxLV291jGlWepwaWZIhjsYibVp/9icUsWb9sc1hU/32+QixR+3EQ+bn8ZefImrGb2zpXsGsi1/jaXQUqxffoyfflYZSb8LcOxmSVTJ4oZpc0UDFTS31BmeEspWi+P7jECZPdqLaeQblOjUVv+znlK6XwJQOdLpZCKlfUKt5SNb1CI5cM2Ft1ir8fTrZazyMEKFrEwc69uE2+h8/z9GRrdiHTUEETYef8tRvPrLqeMr3ZqDbas2i+ATsXFUk/KhB01XJvPJ3EWKWbxMdL3lStc4GJy8rjDYvoODjIUZj3ubXFEckBb1MNb1Gi/YkLT6VXJUX01x7ix+2+2E+/CVCVsAF8fOlcnbYbmD6g010JB7AvKyJpj3pPA40ZoZ2EmXcUpx2x7LLtojk5zeJUmoYUnTR1/UqQuDpKtFjcT5tIQLBTUm0tWXxncfLLPzbjK5ie+52FrH820X4T1+nfUxBdZEtrX9koFW6cmdxFkK98Yh4/1wPIXoFK41PYOSk5TPFQrZuPEtfpIjV4dP0basjaLCQ1RJ3wrLXURkhwye4kGF1KYL1yKBoLTfBZbEJrydv5MBsOTkPxml0bsXLzJeSHQ10F99C8DyKqayRdxJ0ZFdewqI+DAu9EsEw6SPuaqjD/uI1OtPtyWEuqu1/8kgzSsyTn7gSlUeZFEz31xNycgwHP4GSgxE8OJGGdHcggmqeQQz0vsLat8Lp1N+iKzaXyDQ9AUpXHMy+x2VDDOPlj1hgXkDNuIpYxzA+VE1TdSedNc9aEHbKtKLb2WjOS6SkTX+FoNazyDqU+3EdZGk1fLrXAocKW9ZHtrM+IBzTDY+RTTxBEXyDLZVyBFXHX+KSsSPktQeR4fIGDz3ayWwewONYFTOlHjQXv4DZjUH6k64z66VU3Iuj6Z+XjbzInlNLbyOUuNeIfZtMqFWXMycvApe8Eu659OO3UonvXTuOJ0tICJcyFW+gxzQHH7Ubn8TJMfpmJurUQQS9WYOoKRwj1CwY9rjTYjKA8e5mRuwOEaIPZ1lUJmVn/mHqdCnO6lEmEgMIzfFhdvkxlgk9CEF+b4rDt0c5bvkvz165yYr6YBJqnuOdX0RofwX5/Q7s65bQa1NK8u9eJG7RM5Lry1zfJBonLBGeWlqJsrI6HBSrufowgJZ7dkgz13D5o0RWZSwhSqKiQTOf7enRGDLDSMl/wOXIzYRJWjlnEc//kOeMzeifwnsAAAAASUVORK5CYII=

   Image 4
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA75JREFUOE8FwQs0lQcAwPH/Z8Kaeayax8pJSU1ea1y1PK5S0wMn8zwc1zqqndhqhLC43OHOI7VT6zhOrVC2s1RUXtEulYo6lkTmlrM7j2GHKIzw7fcTbNpuii4Rf7Mz8Qc6lfNMWR/jvNY8TmecaX0dz6xKgayhlIXECX42vErNsyOE9kvQr7bHMjEFwaLkG1ERpUftSDzZ1mtIkY8QFnkaBxMVNU3DaCUsQbLrBttXK3k3+SVXtP7C4VwA+ap3UAc8RBhSbRabLkdzf3UG+SMGfKCVR2aiBTkzbgwjcHO4H1O1ilXNA4TXbOSjxjQKje4Q7NfDujYNQkLLdrFEugQ9dR87fIs4eelbPN5/Tdb2r1AeHGFCWs62sjLkVd/RV1iPRplEVEwPtpLLuO30QshamyT6VXRxQtQhLCIDl7opLJwUVMbeYEWulLFXo2hdf451aD5rN+pRfm2IrSu8yJ2W4/T1NYQvF8zFce3zlFt00V/WSu3pdlZOJLA4zR/5GQnHYx25P55PjfwwuncvMFdaScimTnpM91K0xxIh7mKcqDllSqjDGF+EXGB+URql/leJ1owyFDtGnlcWmYaxtIWdQOZznQ36WwhWBXLKy4dfIp4iKHSDxf0dniS/iGLUygepsYRZb4GlkSY0fHyUwcBiTAPiCDs+yNBPjsTYN3J7wpVqaRUN6scI3dOHxVRNLb1T2oT79nP2TRCLnGUkNSqI/kfDwstCan+7ynq7GmJv7abznhGDz2sp6DKgECVC1UC6OKlKJ3CfOxsCgvCrf0jyZglbx8YY8Bimt/ctkqLFyOZMmFr0gKeHgrCt7GblmnIK/m1B2Phqm1g+Yk1J2hzZfZs5EqZDXoMucr9r3HNXsn7iPuFtL/j80CYyb5uheFBNU7OG4fpituRmI5SaGYo5qmVEG/9OUkIAx9bkMlrvSteqPDJPGuDt+B71O0epe5JGTp0Ht9tbiXDUodszndLgdgRDmykxUX0Fvyc6uJlr49JcQPHSclxD1jJ5MI4zHTOkR/yKwsqBtpsT7PW8QOr+VIL8A5m8YoDw2HuPeFRqTMWPvuQtK8DMV2Df8u9Z2JVJ9skS/Oxt+fPSPK3TMdh4XMZdLcd83SvEGTnLDyQgyIwsRefDj9AdvUhAXBp3c4wI9N6KxyMbWjq6GF/+Bl8zexocz5EXaYXss0/Z4/2WWDs5KVI1gl3LjKjMuENvsz7W/X+wILvF+f8eEDKzg/izC1TUZhE/e53U3R8SE7yCZ6IOn/jPYBw5z4GeKP4HK+KV3D0SHY4AAAAASUVORK5CYII=

   Image 5
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA79JREFUOE8FwQ801AcAwPHvz3RZuVvIVP5cWf+QlEsjHnsU09aq8dpyW+Xs6LFc5f9Veo+tub2L8NrLvScaUk29vLsyO38alSJGWqStURn9oV6sodZvn4/QpwsSTccbmd5jTcaAhnMvvUnu9EJyIB1Znie7I//i63E5JzwdmHd5KQ3SSA5MuTG8zo9Db6sQ5DVxoiKvDIeL7nxTGMD2j65w3tMH0+p1HHn9OQvryqnMamW1uhRZ0XXmF29jZ90gM69VkOE6hpCfbC9O83uBzdJ4Uuy/wPSxmTJFPZZ27lRVPKBRtGYqtot+tYp/O0ZozS+k11hC6IUSQrUXEJp+LxW31PsS+LQAw4JJxrbuY0+3C3LtRm66OtEnt8BXpiekc5z2kxJqn0RgNauYPa/OYntvJULO2UHRy3IFRf52LP7yPvLxVWxYPkS4JoZI78182pmBx+RiIt7T88OwyOZqCW/cqkm/JKUrpQVhROkhmo0KLi5L4aWijGl1arAbp86igdTCHJIGH9OsjeZXuwGyo55z7ueZjG41Iz11kQdzAxG+cq4SY7VS4uM+wDLoPrbBLsyXF7F2xhi3nLr5T7mJ4fRwBv8+jvumD6ncu5DMWdtw74pDEhaMULxskXiksJ2kgMdodziSlW1Fx4138Q+soUHlQMbUCcrTMllSNcw9rKnTlHJrez9lBbvYSC+CResnYtOl+bhKC9FYnmRo2QN2xP+GLOoVfn+Uoys9i9S3B4ejXoykJGD0WYOheoqstdGsUhoQYieuiHtC9tIc60rrXEcCjDe57XKUeSu7+O5IH2l7C7ic+AxdyWVyXRYQnDgDp/wE1jc+5K2JUQTJklExv/IqE20z6YlZi7RWxpaRep7sysZGreJMymEG3I/hrSmgLUrCc+EMvcnTOZhUi+3uMYRvFxnE1tQQNO+sZqntAvbv7mVcl0u04ws8pBGULHej5dRrFHPuEFBrR2h6DLMf3WWnXkHb6HSEX54qxKq0aNThiXiWj7FBOxvzOWf63NTIr27D1OzICn03LU5hhNnfxsdYi/eogLeVFS8PJiC0fZYodiSU0JM7j13x39NrCKSluZ+fTs2hwWhg8EYep2V9OJxuZSinGpPSmdlrEkhuuEvNw/sILr7HRBtFOalV3TS+OY9+fT/NIypys73RH6sk4H0Jxef/IaRChbXMl+XDGpRb4tCK+/gxTodgtmoXI0fMRJidGffIZCAtCK/Sa6TqJkk3dVJzJ4u8lRquP/sTz/07OOw/h0eJsVhfb0LZcYj/AaOAhMNcXoqhAAAAAElFTkSuQmCC

   Image 6
   Length: 1390
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA7xJREFUOE8FwQ8w1QcAwPHvT16MylsehUL1iCPtRW/zaMlUr0k6Ozr/5jVDjFf+Vc9tcq2iPzQlUxxD+qd6p23OuVotlblEluZvJbSMpObGZuO3z0eoWaUWT/01gZl8FL9mP555ZmMS+hz7+HhiPw/BfqSYdXU+WAwPsS01haW223m/7gBavzE258cgrNzYIYp5W9EYpbJjuJolnZN8t8aawshSrGyb+Nf3KtfCrnJ6YoYvXf+hZyADyTFnChcl82yDJ0JcT4JooFrF61eJmG3S4l6RzLBCTaWjhL6fvDGx8GDcSIXRwBSRr6c4XX8dq6ECpJJpelW/I3Sr/MWUmrcEjM7HrN+RU/JD3E5pQHZqI383ZrJlupvJsa/J2ZKG3MWV2KfnqbyWQYepFw035Qjfn1gmSs1qcSpwI3zaAfP8Ee40VjBc4oDlvDp27/fj3FYpXg8n+ea3l2zruUSesxOr5DoelAQiuLt0iTEbcthhGMX6e3GULhvlTddbqg0HsQ+5SXu9SO2+zQRnJnElMZ60nUWYtsyh0biEuB+qEEYddomXmjRo89tx2RmGt2YXq6POoNXtZZFrP8eevuKRfhaHPzJlqF4gsWoS6cefsMYgnXtzbyH8XOwjFqaMEzGRhrV2Kb/eaUUepcI6wYG23hAK5q5lfjQE9ijIGMwmPzUbGyGWNjs7WiUxCBef3BJ9Qqd4vmkNgb2BLI8exsBukOS394l6HMOPidW02S4kv2KGOYs9CDXP4R3fXt5riGDBOiVCtaOluPZYGkcDHxG+SU+xcxd9/XI0n72LMmE75ZdHaPR9TJhnOi2ZLlwOSGMot4aj/ympNzyC0Cy1Eg+anKe0UMc5NQTZaOkae4CspIkLu57wbdV9jBvu0TLRily5A/fyONTauzSXyVjR5oWgfFkmJpcqWay6RlB6CnvSddxYvh+F/xIUJeVMJzihOd3NeHQQNntm0zUQwd3WCvSPb3PgYCeC9Sy9mFN0iNgNofTJZpDWBBNdexh7j2z+mO1NpaUxF88e5mTBh3zaIVBZl0XYwwG2ZYWy940MwW33LDE4OQ/N2ELiZV9QFG7CMvMT1LY0kHU7iVQHdzqTwnAby2ZBfym+gzNUnvOiysKV8YXjCD52FWJ0tw7bWkM0+75CUheCXszF/hczAsymOPOgCH+vTjquBFImyyLJLgy6X3BjxXEG/vwAQV0/TxyeI2fr6nZ0192wUKzkZEsPkXZ+tCetR200TdaFtRyvVFB21hLzIhsk+hxyX2QTOT3J//pDf5OspeyaAAAAAElFTkSuQmCC

   Image 7
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA79JREFUOE8FwQs0lQcAwPH/d0+tXJR2I2qOx0ZHjpVL2crcxo0jIa28H1fWyGxWsiV6cJPHOTJJ1pJacWu7iVWz9JLKjZbdrCbyaIeUpY4kpVHffj+hTZ0uVjrN4+2BQtyvnaLHVI/mdiiPZI34HU6mYbY/b40NqRZWkFS9iyV5dwkfvIxiTjhJ6kiEiQwjcUN5DwEpA1xp6eb7yGd0/p3F8nsyXu1LY7Lcl7EV7RzTxmAmHmKtjY7FKg0X5m3EPMcQQRkSLMY1GnO81Y2SGj171msYf6kgbMEywhIXEOjxAEeJF4oFseRfTWeNcR7jNhO4n6rnnNd2hL5LDeLB6PkoF71B8WYQjVLKtKcm2O10wmmqM1v07Sju/4z4tQ/S7C9JKHNhOD2IQD9H/tlajWAyuVG0WL6FmyPv0rtwP2q7fozMXmOa8B3N8a78ZOJJ5clXLHWRkX7Hl+i6YXKkBjjIXXmyqhtBuWGlePFEFreue+LXvZCsGksGm5qZeqae8Q9a2FuzhKhWKTaZ/nRURKA3k+EXc40Ug0AeWNsjSPe7ip7HRunrrWRxUwVHq2V0XVBgOjeOSHcTbnSsZWyZEVlJVrx3dD4SrYae/IfEu9oRYT6O8PiEt9in/YY5F9X0XW3H7bIUfb4vMscR7mvW8LS+nbPWxgwUGRBnomakM5Su1btp3XGDNJsIhEnuc8XsKEcOhcTTuu0HDhxIZEqelqGOUvbXd1E3Uo7Coo3DusfMkJbgUbWIsowhdLcy+FgXhrDJ/6kYfOQvuqd7kxwwSkZxKaPGT0hu/orrtuvplNgyXlfOwaJvMavNpNFGiedZCQEOGv7V6RGyBuJF2z3n2ew0g+RLdszKqSH8swLKY8qxk1thJNhj76hG23YFXckRor/o5fPRbgqfzeT9VGeEKRPTRM3GTMpep5Ec3k1B2CqCd27FqvMOkYvDOZ3QhuxDNX9UzObtcDwn/8xl5fR11DZZkh1hgVA0KVs8f8+ZyVUhWLxQ4bFdxeGBWmqyd3OuNx/lbxBFIX3WBfSnOvFIcoPV4io0g608n+6PkJI0IF6JHiMkpZlHPcW8KJ1F8LZhzCvP8KBHh8/DdbiWvmT1tc14dZ0g+PZWfgxIJDvTh7TnvyNYbQsXoxreocElCcVHd0n8NA/nhHMYeq2j/74cVaeKpNYxDmqPk7cjnSO5vzKz2RrLFnOCJP0Iqa8lYrHEkr2x5xlaKqerMpBf3DxwlH9C1SZD/osNwju4hbsTNtSGKuloOk2um4p9Nx0wUozwPzroi4RFAPHqAAAAAElFTkSuQmCC

   Image 8
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA79JREFUOE8FwQs0lQcAwPH/1wlj8qitGs1WnZQrocJaE3ogVORxSVrN4qJpC3mVc6fuctxND3YusQxjzaO6ZpLMe7lKnAqZnVg6K8/lMe2wnX37/YT6hjIx/Lt/UI9Gs90lHROfeiSXZhhb8x9TAzuZLMhiqrWIBQX53Dh8nlNnjclojGDJdR8Otw8iWJhfES1msqmxzWL5wDKS1TnsP+TGNacELjTOkfe3NpqRZjYt+IXKai969+ux1dkUVdMBOnRAKL1YKMY6hpK76im6JuFolXzCVHMSV1srMdDNZucTNZ8mGRMwcIdVqUbYBv+BpGQYzeN82h50IUxfjxczu0RM1wziJSnHLU2Ft1MFsvuF/Gv1I34XlahX6JOTbMoZX3ciggJJDfgY+9e2MDPcjFBVEyRqDXeQYeyCdNIFi/UTnBwqof10COL37UzHeiP//SFxkds4X2hGzGgm9Qcz2TW2nUsGSQjzIcfE0d6bFPnmE3svkukBG47m5+LgOkvdZw08905AvieIgw46/FzuQUptFT3qEc65vEtqcDfC8eR94nxECdptDqhWbeBZVB4nRsLR6V/EnmYF+pH7qO40I+PkGJVCMU1nrVC0WXKkYZZi+wcIp5w2iJuzq5m/FU3MZBYZy62I2PsC3XsfsbBbgULzFBfDr+m3aKHAT0XLqCtXUr5h47F67ssvIWR1vBJfLm+k9IAbSbuakGxexOdFvii/SkdWLWNoy026zD9k2cxd6qpWUFOhT1/ABRIk61hXehTh5G8V4sa1K1lyppWtnv6U3bmKRdoDHr8q54h2Iz5h84TmWyLJ1UdpHkWBfiSe7rcpd3iLEbUUYYfSVrwhk/PcJxD5XkPU1THIDtTjH2pAdb+CZXpSFqt34/WXhlTpGzhbPMJAk0zlmyFIo/IQLsdsEhfW7mMufBGu7fsZ7DYmQC+enMsKZsvrSFR1U1NrT/EPFfx0fzNN4124Pmmj23UlrUETCM4JA+KJlDiyKqYxiC9HudsIbV13ro3702lbT/KwETUjIVyosyGkVyDbYwfRPe+g5fkC51ANwjn5iNjudojEpUvRq1NhMxZIWfA2JI3+pDs6ojQ5TkvBatylBThlpPKloR1hL3/FJzUR5XQOQoyvWrx78yHfSsKxHMzmg75HPLv1Ht6BaSRK+6hs9mDcKJ61Q4lYbcpg0rCH9RM7CF0ST5yiE8Estlh0+dMTXaf3MTxtj8a6ldV2FVgvjsJvl4bYolKs5ds58uw2srAuvLc6ofXF26jnwrEzeZ3/Afcci6kkppN8AAAAAElFTkSuQmCC

   Image 9
   Length: 1394
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA71JREFUOE8FwQ9UzAcAwPHvTzatIZeydnWOeNKIcZaUiuQ9EZNu9vRE1N78eWlJXdNahv7p1XRGcf1h6iVnuerUcim7XLXkX8J4pVGXPyV/kp7W89vnI7TlmsUP0hKEW9kcmTMds4MdQTk6Mn58QOuGft6E2uKZHEq70Q+vcwJ6u5tIZv3F8YkrkXnHIDiFuYs2hhzC1zqTM3SVlzGN+Om01DtFstazly+viXS2BNIR58HQtkqUB13Q5Bzgek8x6h3VCK5ZLqJ6xnI+WOqZekCCR+oIO19c5e70OnQLavA5ls8ri71EnL9Hcd5S4jx7GXBy5QvNdvLvFyE8tnAVDX1HCXnfQ0PuAB92NNI1zx9NQT+SzG4ajDEEpqURW1vIir6/Gdtbhil3IWH6O3gN7Uc43RkvCrERhGTsI1UbjHycmYsD9Uyd68DBRhtOnK0i4J9cnGelECVrxj38MArlMxKvtzHyzVWEh92XxabUxcxqL2e14QVfxz7h0Egp7arjOHW4M9rwPelWJdwNcmTPYBInpkiYGnoSa3stYXuMCOsrDouLFM9InZ+ATaUJLz7Ha/glbyc28VPbLrzFdnzG6Gix1ZDeb4lL73hOJwRTfdYFW2Ezws6q/eKZi5vQFT7it4iF+MaN5vLt1wTU/UH8iRo6e64gXTmTpFI1E8qLcS51QKnfx7Gkcpom3UIwm4LEyisVfHz/OoNhvxAe+i2ZciMRLKbFqZzXlnUoB7Ygbw4ksy8Rj7LP6DJ3cl46gezg2wj9trvFB49WMs36MdLl22kbUlOv+RNZhi3SwPW8VchQZIfhs8Gaol/HUOtSzJ2+J0zpGkXxuWQEmf9GMdHCjzmFU2BrE4NWHxGvmsze/xSEZM7GX63CfjgDLFqpNeYjJvmw+4ceyj1nkLJUj4B9o/j8jYG5NZeIrPDj0vNPWbMqiaTsEG6cKmJjwDuygo6wLc6R8TPf43z6FIUZveTNiGW4/SJClClYdJtvQcK7POTRDqQYXlClzeJMzHi6y6y4UP8dQ2ercdxzkoSnS0jc1MNY3z7WiBpKpEsQJN4FovnmW+RHV7DF2EbU9tU0HxlEGa0iatxiol96ELiwgxvuozjwtBXf7p/xt/+XmtYN5KtjEQrctOK16nVc0FpRamPCUbGAJyPpZLm0sHnrcZKnrSV3VyUdy1RIGjxZp5MT7R6PtWky8/Q2CF8tWyAeM2v4ffge/nnxdHecRzpJhqvaiKrWn1ebVuHtbEn4yUo+MUayyMuNh7ODsLNPY5lCyf8zHpDai4lAggAAAABJRU5ErkJggg==

Patterns:

* The length varies. Here we see 1386, 1390, 1394, and 1398.

* They all start with the same 87 characters.

* The data gets encoded as Base64.

I was curious about the frequency of each length so I generated a million images
and recorded the occurrence of each length. The result was normal-distribution-y:

.. plot::
   :show-source-link: False
   :include-source: False

   import matplotlib.pyplot as plt

   x_values = [1370, 1374, 1378, 1382, 1386, 1390, 1394, 1398, 1402, 1406, 1410]
   y_values = [0, 7, 351, 7600, 77505, 314079, 450380, 145508, 4555, 15, 0]
   plt.figure(figsize=(12, 6))  # Adjust figure size for better readability
   plt.bar(x_values, y_values, width=3, color='skyblue')
   plt.xlabel("Data URL length")
   plt.ylabel("Occurrences")
   plt.title("Occurrences of data URL lengths")
   plt.xticks(x_values, rotation=45, ha='right') # ha='right' aligns the top of the label
   for i in range(len(x_values)):
       plt.text(x_values[i], y_values[i], str(y_values[i]), ha='center', va='bottom', fontsize=9)
   plt.grid(axis='y', linestyle='--')
   plt.tight_layout()
   plt.show()

Presumably a 16x16 grid full of ``rgb(0, 0, 0)`` would have length ``1374`` whereas
a canvas full of ``rgb(255, 255, 255)`` would have length ``1406``.

Turning to some relevant specs and references:

* `data: URLs <https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/data>`_

* `RFC 2397: The "data" URL scheme <https://www.rfc-editor.org/rfc/rfc2397>`_

* `HTMLCanvasElement: toDataUrl() method <https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL>`_

* `url = canvas.toDataURL([ type [, quality ] ]) <https://html.spec.whatwg.org/multipage/canvas.html#dom-canvas-todataurl-dev>`_

* `Base64 <https://en.wikipedia.org/wiki/Base64>`_

* `RFC 4648: The Base16, Base32, and Base64 Data Encodings <https://datatracker.ietf.org/doc/html/rfc4648>`_

* `Bitmap <https://en.wikipedia.org/wiki/Bitmap>`_

Yields some more useful info:

* As the name implies, the Base64 alphabet contains 64 characters: ``A-Z``,
  ``a-z``, ``0-9``, ``+``, ``/``, and ``=``.

* ``toDataURL()`` basically serializes the canvas's bitmap into the caller-specified file type.

* All browsers that implement ``toDataURL()`` must support PNG.

-------------------------------
Manipulating data URLs directly
-------------------------------

My naive idea was to just generate random data URLs, like this:

.. code-block:: js

   (() => {
     let valid_base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
     const preamble = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAA71JREFUOE8FwQ';
     const total_size = 1390;
     const chars_needed = total_size - preamble.length;
     let data_url = preamble;
     for (let n = 0; n < chars_needed; n++) {
       const random_char_index = Math.random() * valid_base64_chars.length;
       const random_char = valid_base64_chars.charAt(random_char_index);
       data_url += random_char;
     }
     let img = document.querySelector('#static');
     if (!img) {
       img = document.createElement('img');
       img.id = 'static';
       img.width = 16;
       img.height = 16;
       document.body.appendChild(img);
     }
     img.src = data_url;
   })();

But the Chrome DevTools console error'd out, stating that my URLs were invalid. So, for this approach to work,
I would need to understand how to properly serialize PNG data as Base64. I don't have time for that.
Also, the performance of this approach is probably terrible. Constructing each data URL requires a lot of calls
to ``Math.random()``.

I have a simpler idea.

----------------------------------------
Randomly display pre-generated data URLs
----------------------------------------

The plan is "batch process" a bunch of data URLs upfront
and save these into a file:

.. code-block:: js

   const urls = [];
   const canvas = document.createElement('canvas');
   canvas.width = 16;
   canvas.height = 16;
   const ctx = canvas.getContext('2d');
   for (let n = 0; n < 1000; n++) {
     for (let y = 0; y < canvas.height; y++) {
       for (let x = 0; x < canvas.width; x++) {
         const r = Math.floor(Math.random() * 256);
         const g = Math.floor(Math.random() * 256);
         const b = Math.floor(Math.random() * 256);
         ctx.fillStyle = `rgb(${r},${g},${b})`;
         ctx.fillRect(x, y, 1, 1);
       }
     }
     const data = canvas.toDataURL('image/png');
     urls.push(data);
   }
   // Save `urls` into a file…

And then load the data URLs and randomly display a new one
on each frame:

.. code-block:: js

   const favicon = document.querySelector('#favicon');
   function render() {
     const random_index = Math.floor(Math.random() * window.favicon_data.length);
     favicon.href = window.favicon_data[random_index];
     requestAnimationFrame(render);
   }
   fetch('/favicon_data.json').then(response => response.json()).then(json => {
     window.favicon_data = json;
     requestAnimationFrame(render);
   });

.. _requestAnimationFrame: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame

I've known about `requestAnimationFrame`_ for a long time but I think this is the first time
I've ever truly needed it. Achievement unlocked.

-------
Results
-------

Click **Animate** and see for yourself!

.. raw:: html

   <button id="animate">Animate</button>
   <img id="favicon_100x100" style="display: block; padding: 1em 0;" height="100" width="100"/>
   <script>
     (() => {
       const favicon = document.querySelector('#favicon');
       let favicon_request_id = null;
       const img = document.querySelector('#favicon_100x100');
       let img_request_id = null;
       const button = document.querySelector('#animate');
       function animate_favicon() {
         const random_index = Math.floor(Math.random() * window.favicon_16x16.length);
         favicon.href = window.favicon_16x16[random_index];
         favicon_request_id = requestAnimationFrame(animate_favicon);
       }
       function animate_img() {
         const random_index = Math.floor(Math.random() * window.favicon_100x100.length);
         img.src = window.favicon_100x100[random_index];
         img_request_id = requestAnimationFrame(animate_img);
       }
       button.addEventListener('click', () => {
         if (button.textContent === 'Animate') {
           fetch('../_static/favicon_100x100.json').then(response => response.json()).then(json => {
             window.favicon_100x100 = json;
             img_request_id = requestAnimationFrame(animate_img);
           });
           fetch('../_static/favicon_16x16.json').then(response => response.json()).then(json => {
             window.favicon_16x16 = json;
             favicon_request_id = requestAnimationFrame(animate_favicon);
           });
           button.textContent = 'Stop';
         } else {
           cancelAnimationFrame(favicon_request_id);
           cancelAnimationFrame(img_request_id);
           button.textContent = 'Animate';
         }
       });
     })();
   </script>

On my computer (Google Chrome on Debian) the in-page animation directly above this text
seems to render at a high FPS rate. The favicon, however, renders at a much lower FPS
rate.

---------------
Prior art redux
---------------

…

.. _server:

------------------------------------
Appendix: server-side implementation
------------------------------------

In the HTML the favicon was fetched from my web app running on `Render`_:

.. code-block:: html

   …
   <head>
       …
       <link id="favicon" rel="icon" type="image/x-icon" href="https://biodigitaljazz.onrender.com/favicon.ico">
       …
   </head>
   …

``src/main.rs`` contained a `Rocket`_ web app that handled the favicon generation:

.. code-block:: rs

   // I'm a Rust n00b and I leaned on Gemini and Claude to generate a lot of this
   // code, so it's probably crap (but at least it was working crap!)

   #[macro_use]
   extern crate rocket;

   use image::{ImageBuffer, Rgb};
   use rand::prelude::*;
   use rocket::Request;
   use rocket::http::{ContentType, Header, Status};
   use rocket::response::{self, Responder, Response};
   use std::io::Cursor;

   pub struct Favicon<R>(pub R);

   // For anything beyond super basic responses it seems like you need
   // to implement one of these responder things? It felt pretty
   // convoluted, IMO…
   impl<'r, 'o: 'r, R: Responder<'r, 'o>> Responder<'r, 'o> for Favicon<R> {
       fn respond_to(self, req: &'r Request<'_>) -> response::Result<'o> {
           Response::build_from(self.0.respond_to(req)?)
               .header(Header::new(
                   "Cache-Control",
                   "no-cache, no-store, must-revalidate",
               ))
               .header(Header::new("Pragma", "no-cache"))
               .header(Header::new("Expires", "0"))
               .header(Header::new(
                   "Access-Control-Allow-Origin",
                   "https://biodigitaljazz.net",
               ))
               .ok()
       }
   }

   fn generate_favicon() -> Result<Vec<u8>, image::ImageError> {
       let mut rng = rand::rng();
       let mut img = ImageBuffer::new(16, 16);
       for (_, _, pixel) in img.enumerate_pixels_mut() {
           let r: u8 = rng.random::<u8>();
           let g: u8 = rng.random::<u8>();
           let b: u8 = rng.random::<u8>();
           *pixel = Rgb([r, g, b]);
       }
       let mut buffer = Cursor::new(Vec::new());
       img.write_to(&mut buffer, image::ImageFormat::Ico)?;
       Ok(buffer.into_inner())
   }

   #[get("/favicon.ico")]
   fn get_favicon() -> Result<Favicon<(Status, (ContentType, Vec<u8>))>, Status> {
       match generate_favicon() {
           Ok(image_data) => Ok(Favicon((Status::Ok, (ContentType::Icon, image_data)))),
           Err(_) => Err(Status::InternalServerError),
       }
   }

   #[launch]
   fn rocket() -> _ {
       rocket::build().mount("/", routes![get_favicon])
   }

``Cargo.toml`` for completeness:

.. code-block:: toml

   [package]
   name = "biodigitaljazz"
   edition = "2024"
   version = "0.0.0"
   publish = false

   [dependencies]
   rocket = "0.5.1"
   rand = "0.9.0"
   image = { version = "0.25.5", features = ["ico"] }

As well as ``Rocket.toml``:

.. code-block:: toml

   [default]
   address = "0.0.0.0"
   port = 10000

.. _Deploy a Rust Web App with Rocket: https://render.com/docs/deploy-rocket-rust

See also `Deploy a Rust Web App with Rocket`_.

Notes on my experience:

* Render is nice. It's basically a Heroku that's not stuck in 2010.
* I've heard that Rust has a reputation of making simple things difficult.
  Boy, did it live it up to that reputation here. In Python or Node.js I
  would be able to get this running in 10-20 minutes, whereas with Rust it
  was more like 2-3 hours.
* Rocket's incomplete docs didn't help matters, either. E.g. there's no guidance
  on serving images or configuring CORS.
