.. _xrp:

=============================================
Notes on XRP (Experiential Robotics Platform)
=============================================

----------
Background
----------

.. _XRP Kit: https://www.sparkfun.com/experiential-robotics-platform-xrp-kit.html

I received my `XRP Kit`_ from SparkFun on 20250331. This is a v1 kit, not a beta kit.
They don't actually call it "v1". They just refer to it as the "non-beta" kit.

-----
Setup
-----

.. _official MicroPython setup workflow: https://experiential1.odoo.com/code
.. _Reset the flash memory: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory
.. _XRP controller firmware: https://micropython.org/download/SPARKFUN_XRP_CONTROLLER/
.. _XRP Code: https://xrpcode.wpi.edu
.. _wrong firmware: https://xrp.discourse.group/t/micropython-error-during-installation-verification/652/8

The `official MicroPython setup workflow`_ workflow did not work for me. I think
they shipped the v1 kit before all of their docs and quickstart workflows
were thoroughly battle-tested against v1. Someone from SparkFun has confirmed that
some of the v1 kits shipped with the `wrong firmware`_.

This works:

#. `Set up the hardware <https://youtu.be/5GH6TYV_jVU>`_.

#. `Reset the flash memory`_ on the RP2350.

#. Drag-and-drop the latest `XRP controller firmware`_.

#. Go to `XRP Code`_.

#. Select ``MicroPython`` mode.

#. Connect the XRP to your computer over USB.

#. Click **CONNECT XRP**.

After this I was able to run through ``//XRPExamples/installation_verification.py`` on
`XRP Code`_.

-----------
MicroPython
-----------

* `XRPLib <https://github.com/Open-STEM/XRP_MicroPython>`_

https://github.com/micropython/micropython/tree/master/ports/rp2/boards/SPARKFUN_XRP_CONTROLLER

Bootloader
==========

In `Set program to run on boot <https://xrp.discourse.group/t/set-program-to-run-on-boot/671>`_ I learned
that `XRP Code`_ puts some wrapper code around your program when it uploads it onto the board.
``main.py`` is the file that MicroPython actually runs. It looks like this:

.. code-block:: py

   import os
   import sys
   import time
   FILE_PATH = '/lib/ble/isrunning'
   doNothing = False
   x = os.dupterm(None, 0)
   if(x == None):
      import ble.blerepl
   else:
      os.dupterm(x,0)
   try:
      with open(FILE_PATH, 'r+b') as file:
         byte = file.read(1)
         if byte == b'\x01':
            file.seek(0)
            file.write(b'\x00')
            doNothing = True
         else:
            file.seek(0)
            file.write(b'\x01')
      if(not doNothing):
          with open('/XRPExamples/installation_verification.py', mode='r') as exfile:
              code = exfile.read()
          execCode = compile(code, 'XRPExamples/installation_verification.py', 'exec')
          exec(execCode)
          with open(FILE_PATH, 'r+b') as file:
              file.write(b'\x00')

Servo
=====

Starts to crap out at ``207``. Why?

`How servo motors work
<https://www.jameco.com/Jameco/workshop/Howitworks/how-servo-motors-work.html>`_

STAT LED
========

Not really sure how MicroPython accesses it.

Pico SDK sends SPI command to cyw43-driver to control it. https://github.com/georgerobotics/cyw43-driver

In schematic it's called RADIO_GPIO0

MicroPython seems to call it BOARD_LED or EXT_GPIO0 https://github.com/micropython/micropython/blob/master/ports/rp2/boards/SPARKFUN_XRP_CONTROLLER/pins.csv

Can't find SPI code in MicroPython

Maybe here https://github.com/micropython/micropython/blob/3805e65ed3b7306329bf0305d5b46f08d7619a11/ports/rp2/boards/make-pins.py#L14

Hypothesis: pin mismatch between Pico 2 W and XRP for communicating with CYW43 over SPI

Correct!

Also, they've started adding support in Pico SDK https://github.com/raspberrypi/pico-sdk/blob/develop/src/boards/include/boards/sparkfun_xrp_controller.h
