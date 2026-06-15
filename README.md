# Timegrapher PreAmp

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

## About the Project

| ![Timegrapher PreAmp](https://github.com/fabemit/Timegrapher_PreAmp/blob/main/images/Timegrapher_PreAmp.png) |
| :-----------------------------------------------------------------------------------------------------------: |

Timegrapher PreAmp is the **through-hole** piezo preamplifier board for the
Timegrapher Studio wristwatch timegrapher. It conditions the faint escapement
signal from the piezo pickup and feeds the I²S ADC on the
[carrier HAT](https://github.com/fabemit/Timegrapher_Hat). This is the
hand-solderable variant; an SMD version lives in
[Timegrapher_PreAmpSMD](https://github.com/fabemit/Timegrapher_PreAmpSMD).
Designed in KiCad. See [DESIGN.md](DESIGN.md) and [BOM.md](BOM.md).

---

## Repository Contents

This repository contains the KiCad design and production files:

- **`TimegrapherPreamp.kicad_pro` / `.kicad_sch` / `.kicad_pcb`** — KiCad project.
- **`Preamp.kicad_sym` / `sym-lib-table`** — schematic symbols.
- **`Production/`** — Gerbers, drill files, and the fabrication zip.
- **`TimegrapherPreamp.step`** — 3D model of the assembled board.
- **`TimegrapherPreamp_sch.pdf`** — schematic PDF.
- **`gen_sch.py` / `gen_pcb.py`** — scripts used to generate the design.
- **`BOM.md`** — bill of materials. **`DESIGN.md`** — design notes.

Refer to the `CHANGELOG.md` for details about updates between versions.

---

## Timegrapher project

Timegrapher Studio is split across several repositories:

| Repository | Contents |
| --- | --- |
| [Timegrapher_OS](https://github.com/fabemit/Timegrapher_OS) | Desktop application |
| [Timegrapher_App](https://github.com/fabemit/Timegrapher_App) | Mobile companion app |
| [Timegrapher_Firmware](https://github.com/fabemit/Timegrapher_Firmware) | ESP32 device firmware |
| [Timegrapher_Hat](https://github.com/fabemit/Timegrapher_Hat) | Carrier HAT (PCB) |
| [Timegrapher_PreAmp](https://github.com/fabemit/Timegrapher_PreAmp) | Piezo preamp (through-hole) (this repo) |
| [Timegrapher_PreAmpSMD](https://github.com/fabemit/Timegrapher_PreAmpSMD) | Piezo preamp (SMD) |
| [Timegrapher_Stand](https://github.com/fabemit/Timegrapher_Stand) | 3D-printed stand & fixtures |

---

## Learn More

### Documentation

Build notes, BOM, and assembly guides can be found here:
[ThisOldScot Docs](https://thisoldscot.com)
<!-- TODO: replace with the real docs URL when live -->

### ThisOldScot Community

ThisOldScot Community is a great space for the maker community — get answers to
your questions and solutions for our projects there.
<!-- TODO: add the real community/forum URL -->

### ThisOldScot Discord

Another option to get help and advice from other makers via the ThisOldScot Discord.
<!-- TODO: add the real Discord invite URL -->

---

## Contributing

Contributions are welcome! Here's how you can get involved:

- Submit pull requests to enhance the design or fix issues.
- Report bugs or problems by opening an issue.

We encourage community collaboration to make this project even better.

---

## About ThisOldScot

<img src="https://github.com/fabemit/Timegrapher_PreAmp/blob/main/images/ThisOldScot_Logo.png" width="200" alt="ThisOldScot logo">

[ThisOldScot](https://thisoldscot.com) enjoys designing and making electronic
products and projects for enthusiasts, from hobbyists to professionals — boards,
sensors, hobby equipment, and anything else that catches my interest. Every
project is designed in-house and built on open-source hardware and software.

---

# Support the team
We :heart: doing research. New hardware (e.g. oscilloscopes, logic analysers,
servos, PCBs) is costly. Feel free to support us and accelerate our research.

Dev | ThisOldScot |
--- | --- |
Buy me a coffee | <a href="https://www.buymeacoffee.com/"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" height="20px"></a> |
Ko-fi | [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/) |
<!-- TODO: add the real Buy Me a Coffee / Ko-fi URLs -->

---

## License

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike
4.0 International License. Read more in the LICENSE file located in this repository.

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

---

**Disclaimer:**

These designs are provided "AS IS", without warranty of any kind, either expressed
or implied. The entire quality and performance of what you do with the contents of
this repository is your responsibility. In no event will ThisOldScot be liable for
any damages or losses arising out of the use or inability to use the contents of
this repository.

> [!WARNING]
> Use responsibly and at your own risk.

---

## Have fun!

Thank you for your support from your fellow makers at ThisOldScot.

Happy Making!
