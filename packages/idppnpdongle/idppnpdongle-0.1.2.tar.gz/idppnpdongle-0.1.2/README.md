# Inmarsat IDP Plug-N-Play Dongle

The Plug-N-Play dongle is a small programmable single board computer in a
black box intended to be able to quickly demonstrate and prototype 
Internet-of-Things use cases enabled by satellite messaging connectivity.

The dongle connects directly to an **ST2100** satellite modem manufactured by
[ORBCOMM](www.orbcomm.com) and provides access to:

  * Serial communications using **AT commands**
  * Modem **event notification** via discrete output pin to a callback function
  * Reset via external **reset** pin
  * 1 pulse-per-second (**PPS**) from GNSS timing via discrete output pin

The dongle `mode` can be configured to:

1. `transparent` pass through serial commands to a separate third party 
microcontroller (default hardware configuration)
2. `master` act as the application microcontroller 
*(default when using this Python module)*
3. `proxy` act as a proxy intercepting responses from the modem to a third 
party microcontroller

## Installation

```
pip install idppnpdongle
```