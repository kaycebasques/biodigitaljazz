.. _asm:

=========================================
How to program an Arduino Uno in Assembly
=========================================

*2023 Feb 20*

This tutorial shows you how to program an Arduino Uno R3 in AVR Assembly.
The assembly program that you flash onto the Uno just blinks the built-in
LED (pin 13) on and off.

Kudos to `mhitza <https://gist.github.com/mhitza/8a4608f4dfdec20d3879>`_ for
documenting a workflow that actually works.

-----------
Assumptions
-----------

If you don't have the following equipment or experience, you may have
a tough time completing this tutorial.

Equipment
=========

* Arduino Uno R3
* Debian-based Linux laptop that supports ``apt``
* USB-A to USB-B cable

Experience
==========

* Proficiency in Linux CLI stuff like ``cd``, ``git`` and ``~``
* Proficiency in programming a high-level language like Python
* Familiarity with builing binaries from source

-----
Setup
-----

Create the repository
=====================

.. code-block:: console

   mkdir ~/uno
   touch ~/uno/blink.asm
   touch ~/uno/Makefile

Install ``avra``
================

.. code-block:: console

   sudo apt install avra

.. _assembler: https://en.wikipedia.org/wiki/Assembly_language#Assembler

``avra`` (AVR Assembler) will be your `assembler`_.

Install ``avrdude``
===================

.. code-block::

   sudo apt install avrdude

.. _avrdude: https://github.com/avrdudes/avrdude/

`avrdude`_ (AVR Downloader Uploader) will be your tool for
flashing your assembled program onto your Uno.

---------------------------
Create the assembly program
---------------------------

Copy-paste the following code into each respective file.

``~/uno/blink.asm``
===================


.. code-block::


   ; Modified from https://gist.github.com/mhitza/8a4608f4dfdec20d3879
   ; which is copyrighted by Marius Ghita and licensed under Apache-2.0.
 
   .device ATmega328P
   .equ PORTB = 0x05
   .equ DDRB  = 0x04
 
   .org 0x0000
       jmp setup
 
   setup:
       sbi DDRB, 5
       clr r16
       jmp main
 
   main:
       tst r16
       brne off
       rjmp on
 
   on:
       sbi PORTB, 5
       ldi r16, 1
       rjmp delay
 
   off:
       cbi PORTB, 5
       clr r16
       rjmp delay
 
   delay:
       ldi  r18, 41
       ldi  r19, 150
       ldi  r20, 128

   loop:
       dec  r20
       brne loop
       dec  r19
       brne loop
       dec  r18
       brne loop
       rjmp main

I'm an assembly n00b. I can only verify that this program is correct in the
sense that I can see the LED on my Uno blinking on and off. Also when I left
the Uno running overnight nothing blew up.

Resources
---------

Resources for figuring out how the ``blink.asm`` code works:

* `Programming Arduino Uno (ATmega328P) in assembly] <https://gist.github.com/mhitza/8a4608f4dfdec20d3879>`_
* `AVR Instruction Set Manual <https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf>`_
  explains the instructions (e.g. ``jmp``, ``sbi``, etc.)
* `AVR Assembler Reference <https://ww1.microchip.com/downloads/en/DeviceDoc/40001917A.pdf>`_
  explains AVR Assembly syntax and keywords (e.g. ``.device``, ``.equ``, etc.)
* `m328Pdef.inc <https://raw.githubusercontent.com/DarkSector/AVR/master/asm/include/m328Pdef.inc>`_
  is the source for hardware definitions (e.g. ``PORTB``, ``DDRB``, etc.)
* `ATmega328P datasheet <https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf>`_
  provides details on how exactly the instructions need to be constructed in order
  to work with the Uno's MCU, the ATmega328P
* `ATmega328P <https://en.wikipedia.org/wiki/ATmega328>`_
* `AVR Delay Loop Calculator <http://darcy.rsgc.on.ca/ACES/TEI4M/AVRdelay.html>`_
  is the source of the delay and loop code
* `AVR-Assembly-Tutorial <http://www.avr-asm-tutorial.net/index.html>`_
  is a comprehensive, approachable, and delightfully old school walkthrough
  of AVR Assembly programming

``~/uno/Makefile``
==================

.. code-block:: make

   # Modified from https://gist.github.com/mhitza/8a4608f4dfdec20d3879
   # which is copyrighted by Marius Ghita and licensed under Apache-2.0.
 
   %.hex: %.asm
   	~/uno/avra -fI $<
   	if [ -f "*.eep.hex" ]; then rm *.eep.hex; fi
   	if [ -f "*.obj" ]; then rm *.obj; fi
   	if [ -f "*.cof" ]; then rm *.cof; fi
 
   all: $(patsubst %.asm,%.hex,$(wildcard *.asm))
 
   upload: ${program}.hex
   	sudo avrdude -c arduino -p m328p -P /dev/ttyACM0 -b 115200 -U flash:w:$<
 
   .PHONY: all upload

------------------------------
Assemble and flash the program
------------------------------

.. code-block:: console

   cd ~/uno
   # Assumes that the Uno is connected to your Linux computer via the USB-A
   # to USB-B cable and is available at /dev/ttyACM0.
   make program=blink upload

You should see the built-in LED labeled **L** blink on for about 1 second
and then off for about 1 second.

----------
Conclusion
----------

The `insect overlords <https://www.youtube.com/watch?v=8lcUHQYhPTE>`_ are surely
`watching your (assembly) career with great interest <https://www.youtube.com/watch?v=67h8GyNgEmA>`_
now.


