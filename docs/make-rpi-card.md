Setting up a Raspberry Pi for Vision Tracking
=============================================

Our current project uses a Raspberry Pi with a USB camera. To configure the Pi
to work, we need to do the following:

  1. Write the Raspbian image to a MicroSD card
  2. Configure the system to work with a Network
  3. Install our software project on the system

The following sections should describe each step in detail.

Write the Raspbian image to a MicroSD card
------------------------------------------

At the [5][rpi] web site, click the **Downloads** link at the top, and
select the [Raspbian][rbn] button. We want to download the [latest **Lite** version][latest],
as this has a smaller footprint, but does not have a desktop (which we won't need).

Next, follow [these instructions][ins] for burning the image onto a MicroSD card.
Since the site doesn't have any *examples* of what to expect, here is a little help:

Begin by first starting a **Terminal** application, and then running `lsblk` to
see what drives are currently connected to your Linux laptop. For instance, I
see this that I only have a drive called `sda`:

    NAME                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda                     8:0    0 238.5G  0 disk
    ├─sda2                  8:2    0   488M  0 part /boot
    ├─sda3                  8:3    0 237.5G  0 part
    │ ├─ubuntu--vg-swap_1 253:1    0   7.9G  0 lvm  [SWAP]
    │ └─ubuntu--vg-root   253:0    0 229.6G  0 lvm  /
    └─sda1                  8:1    0   512M  0 part /boot/efi

Now, insert a card reader containing your MicroSD card, and re-run `lsblk`, and
I see that I now have a second one, called `sdb`, and that label is what I'm after:

    NAME                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sdb                     8:16   1  29.3G  0 disk
    ├─sdb2                  8:18   1     1K  0 part
    ├─sdb7                  8:23   1  28.1G  0 part
    ├─sdb5                  8:21   1    32M  0 part
    ├─sdb1                  8:17   1   1.1G  0 part
    └─sdb6                  8:22   1    63M  0 part
    sda                     8:0    0 238.5G  0 disk
    ├─sda2                  8:2    0   488M  0 part /boot
    ├─sda3                  8:3    0 237.5G  0 part
    │ ├─ubuntu--vg-swap_1 253:1    0   7.9G  0 lvm  [SWAP]
    │ └─ubuntu--vg-root   253:0    0 229.6G  0 lvm  /
    └─sda1                  8:1    0   512M  0 part /boot/efi

If nothing under the new card is shown under the `MOUNTPOINT`, you can proceed,
otherwise, you need to unmount them, like:

    umount /dev/sdb1  # If that partition had a mount point

Now, we can do the work of copying the bit from the image to the MicroSD card.
Since I am copying to the `sdb` drive, my command would look like this:

    $ cd ~/Downloads
    $ unzip 2017-11-29-raspbian-stretch-lite.zip
    Archive:  2017-11-29-raspbian-stretch-lite.zip
      inflating: 2017-11-29-raspbian-stretch-lite.img
    $ sudo dd bs=4M if=2017-11-29-raspbian-stretch.img of=/dev/sdb conv=fsync
    1772+0 records in
    1772+0 records out
    1858076672 bytes (1.9 GB, 1.7 GiB) copied, 109.374 s, 17.0 MB/s

Remember, to use the TAB key to help expand the file name so that you don't have
to spell it correctly. This command can take up to 30 minutes or longer.

  [rpi]: https://www.raspberrypi.org/
  [rbn]: https://www.raspberrypi.org/downloads/raspbian/
  [latest]: https://downloads.raspberrypi.org/raspbian_lite_latest
  [ins]: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

Configure the system to work with a Network
------------------------------------------

Now that we have a MicroSD card available, plug it into a Raspberry Pi. Next,
connect the Pi to an HDMI monitor, a keyboard, mouse, and power source. What do
you mean, you don't have one around. No problem, and I think we can get this
working.

Take the MicroSD card and put it back into your card reader, and plug that back
into your laptop. We are going to edit some files on the image before powering
our Pi with it.

First, let's make sure it is readable and that we have the correct label, by
running `lsblk`:

    NAME                  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sdb                     8:16   1  29.3G  0 disk
    ├─sdb2                  8:18   1   1.7G  0 part
    └─sdb1                  8:17   1  41.5M  0 part
    sda                     8:0    0 238.5G  0 disk
    ├─sda2                  8:2    0   488M  0 part /boot
    ├─sda3                  8:3    0 237.5G  0 part
    │ ├─ubuntu--vg-swap_1 253:1    0   7.9G  0 lvm  [SWAP]
    │ └─ubuntu--vg-root   253:0    0 229.6G  0 lvm  /
    └─sda1                  8:1    0   512M  0 part /boot/efi

Next, mount the first slot (called a *partition*) on your system:

    $ sudo mount /dev/sdb1 /media

Take a look at the files:

    $ ls /media
    bcm2708-rpi-0-w.dtb     bcm2710-rpi-3-b.dtb  COPYING.linux  issue.txt         overlays
    bcm2708-rpi-b.dtb       bcm2710-rpi-cm3.dtb  fixup_cd.dat   kernel7.img       start_cd.elf
    bcm2708-rpi-b-plus.dtb  bootcode.bin         fixup.dat      kernel.img        start_db.elf
    bcm2708-rpi-cm.dtb      cmdline.txt          fixup_db.dat   LICENCE.broadcom  start.elf
    bcm2709-rpi-2-b.dtb     config.txt           fixup_x.dat    LICENSE.oracle    start_x.elf

We first configure the wireless networking by creating a file in this directory,
`wpa_supplicant.conf`, that should contain this (yeah, you can create/edit this
file with your regular programming editors, like Atom):

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
        ssid="«your_SSID»"
        psk="«your_PSK»"
        key_mgmt=WPA-PSK
    }

Remember to change the `ssid` line with the name of the Wireless network to
connect, and `psk` is its password. While you are at it, create an empty file in
this directory called `ssh`.

When you are done, un-mount the card with the following Terminal command:

    $ sudo umount /media

Take your MicroSD card from the reader, and back into a Raspberry Pi. When you
power it on, it will connect to your network, and allow you to log into it over
the network. The problem is, you need to know its *numeric networking address*.

The Adafruit company has made a nice program called [Pi Finder][pif]. This
program scans the network looking for Raspberry Pi, and allows you to open a
**Terminal** on the Pi (assuming you created the `ssh` file mentioned above) and
**Upload** files from your computer to it. Click the **Bootstrap** button to
install some programs (see [these details][pf2]).

  [pif]: https://github.com/adafruit/Adafruit-Pi-Finder
  [pf2]: https://learn.adafruit.com/the-adafruit-raspberry-pi-finder/overview

Install our software project on the system
------------------------------------------

Using either the **Terminal** button on the *Pi Finder* application, or starting
up the **Terminal** on your laptop and typing:

    $ ssh pi@10.0.1.187  # Or whatever the IP address is

Once you are logged into the system, let's first secure the system by changing the password:

    $ passwd
    Changing password for pi.
    (current) UNIX password:       # This is probably raspberry
    Enter new UNIX password:       # Set to pigmice2733
    Retype new UNIX password:
    passwd: password updated successfully

Next, let's install `git` and the other dependencies:

    $ sudo apt-get install -y git python-pip python-opencv
    $ sudo apt-get install -y python-numpy python-yaml
    $ sudo pip install pynetworktables

Now, we can get the latest version of our code on to the system:

    $ git clone https://github.com/pigmice2733/pigmice-vision

Once you `cd` into the project, test it out:

    $ cd pigmice-vision
    $ pip install -r requirements.txt
    
Remember, you will need to have a valid configuration file, so you may want to
start with the one on your laptop. To copy this, go to the **Terminal** on your
laptop, and enter:

    $ scp .pigmice-config.yaml pi@10.0.1.187:
