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

Have to do this process to get XRPCode working: https://xrp.discourse.group/t/micropython-error-during-installation-verification/652/7

* `Factory reset MicroPython <https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory>`_

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


