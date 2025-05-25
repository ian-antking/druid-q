# ACR122U NFC Reader Setup on Raspberry Pi OS Lite

This guide explains how to get the ACS ACR122U NFC reader working on Raspberry Pi OS Lite, avoiding common driver conflicts.

---

## Prerequisites

- Raspberry Pi running **Raspberry Pi OS Lite**
- USB ACS ACR122U NFC reader
- Internet connection to install packages

---

## Step 1: Update your system

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2: Install PC/SC tools and daemon

```bash
sudo apt install -y pcscd pcsc-tools
```

Enable and start the PC/SC daemon:

```bash
sudo systemctl enable pcscd
sudo systemctl start pcscd
```

---

## Step 3: Prevent kernel modules from grabbing the device

The NFC reader can be claimed by kernel modules (`pn533_usb`, `pn533`, `nfc`) which conflicts with PC/SC access. To prevent this:

1. Check if modules are loaded:

```bash
lsmod | grep pn533
```

2. Remove them if present:

```bash
sudo modprobe -r pn533_usb pn533 nfc
```

3. Blacklist these modules to stop them loading on boot:

```bash
echo -e "blacklist pn533_usb\nblacklist pn533\nblacklist nfc" | sudo tee /etc/modprobe.d/blacklist-nfc.conf
```

4. Reboot the Raspberry Pi:

```bash
sudo reboot
```

---

## Step 4: Verify setup

After reboot, confirm the modules are not loaded:

```bash
lsmod | grep pn533
```

This should show no output.

Plug in your NFC reader and run:

```bash
pcsc_scan
```

You should see your reader listed, and card detection events if you tap a card.

---

## Troubleshooting

- If `pcsc_scan` does not detect your reader, check USB device permissions.
- Ensure your user is in the `plugdev` group or run `pcsc_scan` with `sudo`.
- Make sure no other NFC or USB communication software is running that could grab the device.

---

Now your ACR122U NFC reader should be fully operational on Raspberry Pi OS Lite with PC/SC support!

---

*End of setup guide.*
