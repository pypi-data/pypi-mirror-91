
======
ggwave
======

Tiny data-over-sound library.


.. code:: python

    waveform = ggwave.encode("hello python")


--------
Features
--------

* Audible and ultrasound transmissions available
* Bandwidth of 8-16 bytes/s (depending on the transmission protocol)

------------
Installation
------------
::

    pip install ggwave

---
API
---

encode()
--------

.. code:: python

    encode(data)

Encodes ``data`` into a sound waveform.


Output of ``help(ggwave.encode)``:

.. code::

    built-in function encode in module ggwave
    
    encode(...)
    

decode()
--------

TODO

-----
Usage
-----

.. code:: python

    import pyaudio
    import numpy as np

    import ggwave

    p = pyaudio.PyAudio()

    waveform = ggwave.encode("hello python")

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    stream.write(np.array(waveform).astype(np.int16), len(waveform))
    stream.stop_stream()
    stream.close()

    p.terminate()

----
More
----

Check out `<http://github.com/ggerganov/ggwave>`_ for more information about ggwave!

-----------
Development
-----------

Check out `ggwave python package on Github <https://github.com/ggerganov/ggwave/tree/master/bindings/python>`_.
