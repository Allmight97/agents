# Hardware acceptance reference

The tool proves source integrity, target identity, exact raw-byte readback, and eject. It cannot prove motherboard firmware, USB-port, GPU-display, or bootloader behavior.

For real acceptance, boot the target machine in the firmware mode required by the publisher and record:

- the firmware boot entry and the exact menu or installer shown;
- one representative diagnostic or live image loaded from the menu;
- the display path used, especially when a discrete GPU is present;
- any firmware, Secure Boot, USB-port, or kernel error;
- whether the machine reaches the image's documented first usable state.

Treat these as distinct failures: source/readback mismatch, target identity/auth/eject failure, firmware not selecting the USB, menu/payload failure, and payload reaching userspace but failing graphics or hardware initialization. A VM smoke test is useful for menu and early kernel checks, but does not replace this physical proof.
