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
through the process of creation.

-------------
Random colors
-------------

What if I just generate a random color in every pixel? What will that look like?

.. _Rocket: https://rocket.rs
.. _Render: https://render.com

In my first implementation, I generated the favicon server-side. You can see the full
code in :ref:`server` but I quickly realized that this approach wouldn't work. Or at least,
it was wildly sub-optimal. More on that in a moment.

When I eventually got this first implementation working, I was pretty excited
to see the result:

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

TV static! A grid of random colors looks like TV static.
Obvious in hindsight, but I did not expect that.

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

First, channels. To the TV, "putting on channel 2" meant tuning the video
receiver to a specific frequency and the audio receiver to another specific
frequency and then outputting the data received at those specific frequencies.

.. _cosmic microwave background: https://en.wikipedia.org/wiki/Cosmic_microwave_background

Now, static. The gist of the phenomenon is that old TVs always output whatever
their audio and video receivers pick up, and static is what happens when no real
data is being broadcast over the channel. The TV is outputting the random electromagnetic
radiation that happens to be occurring on the frequencies that it's tuned to receive.
The TV itself generates some of this random electromagnetic radiation. Other electronic
devices generate it, too. And, most cool of all, around 1% of it comes from the
`cosmic microwave background`_ generated from the Big Bang!

Sources:

* `The evolution of television <https://socialsci.libretexts.org/Bookshelves/Communication/Journalism_and_Mass_Communication/Book%3A_Mass_Communication_Media_and_Culture/09%3A_Television/9.01%3A_The_Evolution_of_Television>`_
* `Noise (video) <https://en.wikipedia.org/wiki/Noise_(video)>`_
* `Why don't TVs have static and white noise anymore? <https://www.howtogeek.com/840090/why-dont-tvs-have-static-and-white-noise-anymore/>`_
* `Analog television <https://en.wikipedia.org/wiki/Analog_television>`_

While doing this research, I realized that TV static was often black and white.
Maybe I had an unusual TV that output static with color, or maybe my memory is mistaken.
Or maybe, if I animate the static at a fast frame rate, it will start to look black and
white…?

-----------------------
Animating the TV static
-----------------------

OK, back to hacking. Once I realized that my random grid of colors looked
like TV static, I knew I had to try to animate the favicon to recreate the
full experience. Which brings me back to my initial server-side implementation…

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
