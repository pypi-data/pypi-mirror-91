# venti

## Setting up Raspberry Pi
- Install Raspberry Pi OS onto MicroSD card [instructions](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility/)
- Modify MicroSD card according to [here](https://github.com/hardillb/rpi-gadget-image-creator/)
- Run the following on the Raspberry Pi once booted
  ```bash
  bash <(curl -L http://bit.ly/vent-rpi)
  ```

## Setting up Server / Developer
- Run
  ```bash
  git clone https://github.com/MinRegret/venti
  cd venti
  pip install -e .
  ```

## Acknowledgements
Much of the device code is copied or derived from the [People's Ventilator Project](https://github.com/CohenLabPrinceton/pvp).
