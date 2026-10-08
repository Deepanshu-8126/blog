/* ============================================================
   PC Lab 3D — educational content
   For every part, per mode: e = Elementary, h = High School,
   c = College, t = Tinkerer. Missing levels fall back:
   t → c → h → e.
   ============================================================ */
window.PC = window.PC || {};

PC.CONTENT = {

  /* ---------- Core tower parts ---------- */

  case: {
    e: {
      name: "The Case",
      one: "The box that keeps all the computer parts safe and together.",
      detail: "Just like toys live in a toy box, all the computer parts live inside this box. It has holes and fans so the computer can breathe cool air and stay comfortable. It also has the power button you press to wake the computer up!",
      fun: "Some cases have see-through windows and glowing lights inside — like an aquarium for computer parts!"
    },
    h: {
      name: "Computer Case (Chassis)",
      one: "The enclosure that houses, protects and cools all internal components.",
      detail: "Cases follow form-factor standards like ATX and micro-ATX, which define which motherboards and power supplies fit. They provide mounting points for the board, PSU and drives, and their airflow layout — front/bottom intake, rear/top exhaust — is a major factor in cooling performance.",
      fun: "The ATX form factor arrived in 1995 and is still the standard today; it was created by Intel to fix the messy 'Baby AT' designs of the 1980s.",
      specs: ["ATX", "Tempered glass", "2× front intake"]
    },
    c: {
      name: "Computer Case (Chassis)",
      one: "Housing, cooling and cable-management platform for the build.",
      detail: "Modern cases add cable-routing channels, PSU shrouds, dust filters and tool-less drive sleds. Airflow planning matters: positive pressure (more intake than exhaust) keeps dust out through filtered intakes, while negative pressure cools slightly better but sucks dust through every gap. Radiator support and clearance for long GPUs drive case choice.",
      fun: "A 'silent' case can cut noise by 5–10 dBA just with damped panels and airflow-tuned vents — but usually runs a few degrees warmer.",
      specs: ["ATX", "Front USB-C", "360 mm rad support"]
    }
  },

  psu: {
    e: {
      name: "The Power Box",
      one: "It gives electricity to every part of the computer.",
      detail: "The computer gets electricity from the wall, but that electricity is too strong for the small parts. The power box changes it into the gentle electricity each part needs — like a grown-up cutting everyone's food into small, safe pieces!",
      fun: "Wall electricity would zap the computer parts — the power box protects them from it."
    },
    h: {
      name: "Power Supply Unit (PSU)",
      one: "Converts AC wall power into clean DC rails the components need.",
      detail: "The PSU converts 110–240 V alternating current into +12 V, +5 V and +3.3 V direct current rails. Its wattage rating must exceed total system draw; efficiency is certified by the 80 Plus scale (Bronze through Titanium). The +12 V rail feeds the CPU and GPU — the two biggest consumers.",
      fun: "A PSU is most efficient at 50–80 % of its rating, so an oversized unit can actually waste more energy than a right-sized one.",
      specs: ["650 W", "80 Plus Gold", "+12 V rail"]
    },
    c: {
      name: "PSU — Rails, Modularity & Efficiency",
      one: "Multi-rail DC conversion with modular cabling for clean builds.",
      detail: "Modern PSUs use a single +12 V design (with DC-DC converters for 5 V/3.3 V) and are fully or semi-modular. Rails are protected by OCP/OVP/OTP circuitry. Sizing rule of thumb: total draw at ~60 % of capacity. ATX 3.0 units add the 12VHPWR connector and better transient handling for power-spiky GPUs.",
      fun: "A PSU's fan is usually intake-down in modern cases — it breathes from under the case through a filtered vent.",
      specs: ["ATX 3.0", "Fully modular", "OCP/OVP"]
    }
  },

  mobo: {
    e: {
      name: "The Motherboard",
      one: "The big flat board that connects all the parts together.",
      detail: "Every part plugs into this board. It's like the playground where the brain, the memory and the picture maker all meet and talk to each other. The little silver lines on the board are the paths they use to send messages!",
      fun: "The tiny lines on a motherboard are like a road map where information drives around at super speed."
    },
    h: {
      name: "Motherboard (Mainboard)",
      one: "The main circuit board connecting CPU, RAM, storage and expansion cards.",
      detail: "The motherboard carries the CPU socket, DIMM slots for RAM, PCIe slots for expansion cards, SATA/M.2 connectors and pin headers for USB, fans and the front panel. Copper traces on the PCB route high-speed signals, and the chipset manages communication between the CPU and most devices.",
      fun: "PCIe 4.0 x16 moves about 32 GB/s — roughly 2,000× faster than the original 1994 PCI bus.",
      specs: ["ATX", "LGA1700", "PCIe 4.0"]
    },
    c: {
      name: "Motherboard — Platform Architecture",
      one: "CPU socket, chipset, VRM and I/O in one multilayer PCB.",
      detail: "Board choice determines upgrade paths: socket generation, memory type (DDR4/DDR5), PCIe generation and lane count. The VRM quality decides CPU power headroom; LAN/audio/wireless controllers are integrated peripherals. Budget boards cut VRM phases and rear I/O; premium boards add POST-code displays, BIOS flashback and reinforced slots.",
      fun: "Some flagship boards have 24+ power phases and cost more than a mid-range CPU — overclockers pay for voltage stability.",
      specs: ["8-layer PCB", "DDR5", "PCIe 5.0"]
    }
  },

  cpu: {
    e: {
      name: "The Brain",
      one: "It thinks and does all the math.",
      detail: "The brain solves all the computer's problems — super fast! When you tap the screen or move the mouse, the brain decides what should happen next. Everything you do on a computer is the brain working things out.",
      fun: "The brain can do billions of little math problems every single second!"
    },
    h: {
      name: "Central Processing Unit (CPU)",
      one: "Executes program instructions — the 'brain' of the PC.",
      detail: "A modern CPU has multiple cores, each running billions of cycles per second (measured in GHz). It fetches instructions from RAM, decodes and executes them, and writes results back. On-chip cache (L1/L2/L3) keeps hot data close; the integrated memory controller talks directly to RAM.",
      fun: "Apple's M1 packs 16 billion transistors into a chip about the size of a fingernail.",
      specs: ["8 cores", "4.5 GHz", "16 MB L3"]
    },
    c: {
      name: "CPU — Architecture & Power",
      one: "Multicore execution engine with integrated memory controller and PCIe root complex.",
      detail: "The CPU links to the chipset over a DMI/Infinity-Fabric style bus, and its memory controller drives DDR channels directly. Power delivery is critical: the board's VRM converts 12 V down to ~1.2 V at 100+ A, and boost algorithms raise clocks whenever thermal and power headroom allow. Overclocking = raising those limits manually.",
      fun: "Under full load a flagship CPU can draw over 250 W — more than a small electric kettle.",
      specs: ["DDR5-6000", "PCIe 5.0", "105 W TDP"]
    },
    t: {
      name: "CPU — The Silicon Die",
      one: "Billions of transistors forming cores, cache and I/O fabric.",
      detail: "The die contains ALUs, branch predictors, register files and multi-level cache (L1 ~32–64 KB per core, L2 ~1 MB, shared L3 in the tens of MB). The die is bonded to a substrate and capped with an Integrated Heat Spreader (IHS). Signals leave through roughly 1,700 pads that the socket's pins contact. Clock signals distribute across the die via H-tree networks.",
      fun: "Modern fabs print features about 3 nm wide — roughly 10 atoms across. A single dust particle on a wafer ruins many chips.",
      specs: ["~20B transistors", "3 nm node", "1700 pads"]
    }
  },

  paste: {
    h: {
      name: "Thermal Paste (TIM)",
      one: "Fills the microscopic air gaps between CPU and cooler.",
      detail: "Metal surfaces look flat but have microscopic valleys. Air trapped in those valleys insulates badly, so a Thermal Interface Material — thermal paste — is squeezed between the CPU and cooler to fill them. A pea-sized dot spreads into a film thinner than paper.",
      fun: "Liquid-metal TIMs conduct heat ~5× better than classic paste — but they're electrically conductive, and one stray drop can destroy a board.",
      specs: ["~5 W/m·K", "Non-conductive"]
    },
    c: {
      name: "Thermal Interface Materials",
      one: "From paste to liquid metal — the bottleneck between die and cooler.",
      detail: "Interface resistance is often the real limit on cooling. Options: silicone/zinc-oxide paste (safe), ceramic (better, non-conductive), carbon/graphene pads (reusable), and liquid metal (gallium alloy — best conductivity, but conductive and corrosive to aluminium). Application method barely matters for paste; coverage matters a lot.",
      fun: "Some enthusiasts 'delid' CPUs — remove the IHS — and apply liquid metal directly on the die for up to 15 °C improvement.",
      specs: ["Gallium alloy", "73 W/m·K"]
    }
  },

  cooler: {
    e: {
      name: "The Cooler",
      one: "A fan that keeps the brain from getting too hot.",
      detail: "When the brain works hard, it gets warm — like you after running around! The cooler blows cool air over the brain so it stays comfortable and can keep thinking quickly.",
      fun: "Computer fans can spin faster than a car engine — thousands of times every minute!"
    },
    h: {
      name: "CPU Cooler (Heatsink + Fan)",
      one: "Moves heat away from the CPU into the air.",
      detail: "A metal heatsink conducts heat away from the CPU, and its fins maximize the surface area exposed to air. A fan forces air across the fins, carrying the heat away. Heatpipes — hollow copper tubes with a phase-changing fluid — move heat from the base to the fins far more efficiently than solid metal.",
      fun: "Heatpipes work like a tiny weather cycle: liquid boils at the hot end, vapor travels up, condenses at the cool end and wicks back down.",
      specs: ["4 heatpipes", "~25 dBA"]
    },
    c: {
      name: "Air vs Liquid Cooling",
      one: "Air coolers use heatpipes; AIO liquid coolers add a pump, radiator and coolant loop.",
      detail: "An AIO (all-in-one) cooler pumps coolant from the CPU block to a radiator where fans dissipate the heat, then back again. Liquid handles high heat loads in compact spaces and looks cleaner; air coolers are simpler, cheaper and last longer (no pump to fail). Neither is strictly better at the same price point.",
      fun: "An AIO pump moves 1–2 litres of coolant per minute and runs sealed for years — the same loop, thousands of heat cycles.",
      specs: ["240 mm radiator", "1200–1800 RPM"]
    }
  },

  ram: {
    e: {
      name: "The Memory",
      one: "It remembers things while the computer is awake.",
      detail: "Memory is like a super-fast whiteboard. While you play or draw, the computer writes notes on the whiteboard so it can find them instantly. When the computer goes to sleep, the whiteboard gets wiped clean!",
      fun: "That's why we press 'save' — to copy important things from the whiteboard to the storage box!"
    },
    h: {
      name: "Random Access Memory (RAM)",
      one: "Fast, volatile working memory holding running programs and data.",
      detail: "RAM is DRAM: every bit is stored as electrical charge in a tiny capacitor that must be refreshed thousands of times per second. Modules plug into DIMM slots; two matched sticks in the right slots enable dual-channel mode, doubling bandwidth. Capacity is measured in GB, speed in MT/s.",
      fun: "DDR5 starts at 4,800 MT/s and runs past 8,000 MT/s — early DDR4 topped out around 2,133 MT/s.",
      specs: ["16 GB DDR5", "Dual channel", "6000 MT/s"]
    },
    c: {
      name: "RAM — Channels, Timings & XMP",
      one: "DIMM population rules and why RAM speed is a latency game.",
      detail: "Populate the correct slots for dual-channel (usually A2/B2). Beyond bandwidth, latency matters: CAS latency (CL) is measured in cycles, so 6000 CL30 and 6400 CL32 are nearly identical in real latency. XMP/EXPO profiles are factory-overclock presets; stability depends on the CPU's memory controller quality.",
      fun: "Server RAM (ECC) has an extra chip that detects and fixes single-bit errors — cosmic rays really do flip bits.",
      specs: ["2×16 GB", "XMP", "CL30"]
    },
    t: {
      name: "DRAM — One Transistor, One Capacitor",
      one: "Every bit is a capacitor holding charge, gated by a transistor.",
      detail: "Each DRAM cell is 1T1C: a transistor gates access to a capacitor storing ~30 fF of charge. Charges leak within milliseconds, so rows are refreshed every 64 ms. Reading a row is destructive — sense amplifiers detect the faint signal and write it back. Banks, rows and columns are addressed in bursts for throughput.",
      fun: "A 16 GB module holds ~137 billion cells, each storing only a few thousand electrons — reading one cell means amplifying a whisper.",
      specs: ["1T1C cells", "64 ms refresh", "8 banks"]
    }
  },

  storage: {
    e: {
      name: "The Storage",
      one: "It keeps games, photos and videos safe — even when the computer is off.",
      detail: "The whiteboard (memory) forgets when the power goes off, but the storage box remembers forever. Your games, drawings and photos all live here, waiting for you.",
      fun: "A small storage box can hold more pictures than you could look at in a whole year!"
    },
    h: {
      name: "Storage Drive",
      one: "Long-term, non-volatile storage — keeps data when power is off.",
      detail: "Unlike RAM, storage is non-volatile. Two common types: SSDs (flash memory chips — no moving parts, very fast) and HDDs (spinning magnetic platters — cheap per GB). Drives connect over SATA or NVMe/PCIe, and the OS filesystem organizes their contents.",
      fun: "An SSD can open a file ~100× faster than a spinning hard drive — that's why old PCs feel brand-new after an SSD upgrade.",
      specs: ["SSD vs HDD"]
    }
  },

  ssd: {
    h: {
      name: "Solid State Drive (SSD)",
      one: "Flash-based storage with no moving parts.",
      detail: "SSDs store bits as charge in NAND flash cells. SATA SSDs are capped around 550 MB/s by the interface; NVMe SSDs talk directly over PCIe and can exceed 7,000 MB/s. No spin-up, no seek time — just instant random access.",
      fun: "Flash cells wear out after thousands of write cycles, so controllers spread writes evenly across the drive — a trick called wear levelling.",
      specs: ["1 TB", "SATA 6 Gb/s"]
    },
    c: {
      name: "SSD — NAND, Controllers & Endurance",
      one: "TLC/QLC cells, SLC cache and why SSDs slow down when full.",
      detail: "NAND types trade speed, density and endurance: SLC (1 bit/cell) > MLC > TLC > QLC (4 bits/cell). Drives use an SLC write cache for burst speed, and TRIM lets the OS tell the drive which blocks are free. Garbage collection runs in the background — which is why a nearly-full SSD gets slower.",
      fun: "Enterprise SSDs quote endurance in DWPD — Drive Writes Per Day. A 1 DWPD drive can rewrite itself completely, every day, for 5 years.",
      specs: ["TLC NAND", "DRAM cache", "TRIM"]
    }
  },

  hdd: {
    h: {
      name: "Hard Disk Drive (HDD)",
      one: "Magnetic platters and a moving read/write head.",
      detail: "An HDD stores data as magnetic domains on spinning platters (typically 5,400–7,200 RPM). A read/write head floats nanometers above the surface on an air bearing, seeking across tracks. HDDs remain the cheapest storage per terabyte — ideal for archives and media.",
      fun: "The head flies so close to the platter that a single dust particle would be like a boulder on a road — drives are assembled in cleanrooms.",
      specs: ["2 TB", "7200 RPM"]
    },
    c: {
      name: "HDD — Platters, SMR & the Last Mile",
      one: "Why hard drives still exist in the SSD era.",
      detail: "Capacity tricks: Shingled Magnetic Recording (SMR) overlaps tracks like roof tiles for density at the cost of rewrite speed; helium-filled drives reduce drag and pack more platters. HDDs now serve bulk/archive roles while SSDs handle OS and hot data.",
      fun: "A 20 TB enterprise drive reads sequentially at ~280 MB/s — the same speed as a 2008-era SSD.",
      specs: ["SMR", "Helium sealed"]
    }
  },

  gpu: {
    e: {
      name: "The Picture Maker",
      one: "It draws all the pictures you see on the screen.",
      detail: "Every picture, cartoon and game world is drawn by this part. It draws millions of tiny dots of light so fast that they look like smooth, moving pictures!",
      fun: "When you play a game, the picture maker redraws the whole screen 60 or more times every single second."
    },
    h: {
      name: "Graphics Processing Unit (GPU)",
      one: "A massively parallel processor specialized for graphics — and now AI.",
      detail: "GPUs contain thousands of small cores that work in parallel — ideal for rendering millions of triangles per frame, and for AI training workloads. Discrete cards carry their own VRAM (fast GDDR memory) and draw up to 300+ W through PCIe power connectors.",
      fun: "An RTX 4090 has 16,384 CUDA cores and 24 GB of VRAM — more raw compute than a supercomputer from 2005.",
      specs: ["16 GB GDDR6", "PCIe x16"]
    },
    c: {
      name: "GPU — Compute Units, VRAM & Ray Tracing",
      one: "CUDA/stream processors, RT cores, tensor cores and display engines.",
      detail: "Modern GPUs mix shader cores (rasterization), RT cores (ray/triangle intersection for ray tracing) and tensor cores (matrix math for AI upscaling like DLSS). VRAM bandwidth (e.g., 1 TB/s on wide GDDR6X buses) is often the limiting factor at high resolutions. Cards draw 75 W from the slot plus 150 W per 8-pin.",
      fun: "DLSS renders at lower resolution and lets a neural network upscale — the GPU literally guesses missing pixels, and it looks better than native in some scenes.",
      specs: ["3× fans", "450 W", "1 TB/s"]
    }
  },

  nvme: {
    c: {
      name: "M.2 NVMe SSD",
      one: "Flash storage talking directly over PCIe lanes.",
      detail: "M.2 is the form factor (22 mm wide, 30–110 mm long); NVMe is the protocol. NVMe drives get 4 PCIe lanes straight to the CPU/chipset — ~7,000 MB/s on PCIe 4.0 versus ~550 MB/s for SATA SSDs. Installation is a single screw.",
      fun: "An NVMe drive can copy a 50 GB game in seconds — the same job took minutes on a hard drive.",
      specs: ["PCIe 4.0 x4", "7,000 MB/s"]
    },
    t: {
      name: "NVMe — Queues and Lanes",
      one: "Why NVMe crushes SATA: parallel queues over PCIe.",
      detail: "SATA is one command queue with 32 entries (built for spinning disks); NVMe exposes 65,535 queues with 65,535 commands each, mapped directly to CPU cores. The drive appears as a PCIe endpoint using 4 lanes of differential signaling, with data protected by LDPC error correction.",
      fun: "Your NVMe drive processes more parallel I/O commands than a 1990s mainframe storage array.",
      specs: ["PCIe x4", "64K queues"]
    }
  },

  cables: {
    h: {
      name: "Power Cables",
      one: "Route power from the PSU to the board and CPU.",
      detail: "The 24-pin ATX connector powers the motherboard; the 8-pin EPS connector feeds the CPU's voltage regulator. Connectors are keyed so they can't be inserted the wrong way — the classic beginner question is always 'why won't it fit?'",
      fun: "The ATX 24-pin standard has been stable since 2003 — even old 20-pin power supplies work with a small adapter.",
      specs: ["24-pin ATX", "8-pin EPS"]
    }
  },

  cables24: {
    c: {
      name: "24-pin ATX Connector",
      one: "Main motherboard power.",
      detail: "The 24-pin supplies +3.3 V, +5 V, +12 V and ground rails to the board. Each pin is rated around 6 A, and wire gauge matters at high load. Modular PSUs let you detach unused cables for cleaner builds and better airflow.",
      fun: "The extra 4 pins (over the old 20-pin) were added for the higher power draw of PCIe-era graphics.",
      specs: ["+3.3/+5/+12 V"]
    }
  },

  cables8: {
    c: {
      name: "8-pin EPS (CPU Power)",
      one: "Feeds the CPU's VRM directly.",
      detail: "Modern CPUs draw 100–250 W at around 1.2 V — that's over 100 A through the VRM. The EPS 8-pin (rated ~336 W) supplies the 12 V that the VRM steps down next to the socket. High-end boards add a second 8-pin for extreme overclocking.",
      fun: "100 A would melt a normal wire — that's why CPU power travels at 12 V and is converted right at the socket.",
      specs: ["12 V", "~336 W"]
    }
  },

  pciecable: {
    c: {
      name: "PCIe Power (GPU)",
      one: "6/8-pin connectors feeding the graphics card.",
      detail: "The PCIe slot provides 75 W; cards needing more draw through 6-pin (75 W) or 8-pin (150 W) connectors from the PSU. Three 8-pins plus the slot = up to 525 W available. Never daisy-chain more load than the cable is rated for.",
      fun: "The 12VHPWR connector saga showed what happens when high power meets a small connector — always push it in all the way.",
      specs: ["8-pin", "150 W each"]
    }
  },

  sata: {
    c: {
      name: "SATA Cable",
      one: "Data cable between motherboard and drives.",
      detail: "SATA III carries 6 Gb/s (~550 MB/s after encoding overhead). One cable per drive, with an L-shaped keyed connector. Drive power comes separately from the PSU's SATA power connectors — two cables per drive in total.",
      fun: "SATA cables are often the messiest part of a build — cable management is a whole hobby of its own.",
      specs: ["SATA III", "6 Gb/s"]
    }
  },

  aio: {
    c: {
      name: "AIO Liquid Cooler",
      one: "Closed-loop liquid cooling: pump, block and radiator.",
      detail: "The block sits on the CPU and a pump circulates coolant through tubes to the radiator, where fans shed the heat. Sealed for life — no filling, no maintenance. Radiator sizes: 120/240/280/360 mm; bigger rad = more cooling but case-fitment limits apply.",
      fun: "Liquid cooling was exotic enthusiast gear in 2000; today a 240 mm AIO costs less than some premium air coolers.",
      specs: ["240 mm", "Pump + 2 fans"]
    }
  },

  wifi: {
    c: {
      name: "Wi-Fi / Bluetooth Card",
      one: "Wireless networking on a PCIe x1 card.",
      detail: "The card carries the radio, MAC layer and antennas, and connects over PCIe x1 (or M.2 Key E) plus USB for Bluetooth. Wi-Fi 6E adds the 6 GHz band; antenna placement and orientation matter more than raw specs in practice.",
      fun: "Your body absorbs 2.4 GHz signals — standing between the router and your PC measurably weakens the connection.",
      specs: ["Wi-Fi 6E", "BT 5.3"]
    }
  },

  fans: {
    c: {
      name: "Case Fans & Airflow",
      one: "Front intake, rear/top exhaust — the PC's breathing plan.",
      detail: "Fans are rated by size (120/140 mm), RPM and static pressure. Rule of thumb: intake at front/bottom, exhaust at rear/top, slightly positive pressure to keep dust out. PWM fans let the motherboard vary speed with temperature, balancing noise and cooling.",
      fun: "A 120 mm fan at 1000 RPM moves ~50 m³ of air per hour — your PC slowly breathes your whole room.",
      specs: ["120 mm PWM", "3 fans"]
    }
  },

  fpanel: {
    c: {
      name: "Front Panel Connectors",
      one: "The tiniest, fiddliest plugs in the whole build.",
      detail: "Power switch, reset switch, power LED and HDD LED — tiny single-pin and two-pin headers that must match the motherboard's pinout diagram. Polarity matters for LEDs. Every builder has plugged the power LED in backwards at least once.",
      fun: "The pins are 2.54 mm apart — the same spacing as a 1980s electronics breadboard.",
      specs: ["PWR SW", "LED ±"]
    }
  },

  panel: {
    e: {
      name: "The Side Door",
      one: "Close the door so everything is safe and tidy.",
      detail: "Now you've built a whole computer! The glass door lets everyone see the cool parts inside while keeping dust out. Computers love clean air!",
      fun: "Dust is a computer's enemy — it blocks the air and makes parts hot and grumpy."
    },
    h: {
      name: "Side Panel",
      one: "Closes the chassis and completes the airflow path.",
      detail: "Panels complete the case's airflow design: intake fans pull cool air in at the front, exhaust fans push warm air out the rear and top. An open panel breaks this path and can actually make components run hotter despite 'more air'.",
      fun: "Most cases use captive thumbscrews — tool-less by design, so the panel is a 10-second job.",
      specs: ["Tempered glass"]
    }
  },

  /* ---------- Peripherals ---------- */

  monitor: {
    e: {
      name: "The Screen",
      one: "It shows you everything the computer is doing.",
      detail: "The screen is the computer's face! Whatever the brain thinks and the picture maker draws appears here for you to see. Without a screen, the computer would have no way to talk to you.",
      fun: "A screen is made of millions of tiny dots of light called pixels. They're too small to see one by one!"
    },
    h: {
      name: "Monitor (Display)",
      one: "Output device that turns digital signals into light.",
      detail: "Monitors receive frames from the GPU over HDMI or DisplayPort. LCD panels use a backlight with liquid crystals acting as shutters; OLED pixels emit their own light for perfect blacks. Refresh rate (Hz) is how often the image updates; resolution is the pixel count.",
      fun: "Your monitor redraws every frame even when the picture looks still — 60 to 360 times per second.",
      specs: ["27″", "1440p", "165 Hz"]
    },
    c: {
      name: "Monitor — Panels & Signal",
      one: "IPS vs VA vs OLED, HDR and adaptive sync.",
      detail: "Panel tech sets the trade-offs: IPS (color accuracy, viewing angles), VA (contrast), TN (speed, cheap), OLED (per-pixel light, near-zero response). Adaptive sync (G-Sync/FreeSync) matches refresh to frame rate to kill tearing. HDR needs brightness + wide color gamut; specs sheets often overpromise here.",
      fun: "A 4K 144 Hz signal needs ~39 Gb/s — that's why DisplayPort 2.1 and HDMI 2.1 exist.",
      specs: ["IPS", "HDR600", "G-Sync"]
    }
  },

  keyboard: {
    h: {
      name: "Keyboard",
      one: "Primary text input device.",
      detail: "Each key sits on a matrix of rows and columns; the controller scans the matrix many times per second and sends scan codes to the PC over USB. Pressing a key is simply closing a switch at a known matrix position.",
      fun: "The QWERTY layout dates to 1870s typewriters — originally partly to stop mechanical arms from jamming.",
      specs: ["USB", "N-key rollover"]
    },
    c: {
      name: "Keyboard — Switches & Scan Codes",
      one: "Mechanical switches, actuation points and firmware layers.",
      detail: "Mechanical keyboards use individual switches (Cherry MX Blue/Brown/Red…) with distinct actuation force and feel; linear, tactile or clicky. Firmware (QMK/VIA) lets keys be remapped in layers. 'N-key rollover' means every simultaneous keypress registers independently.",
      fun: "Typing on a good mechanical board is measured in 'thock' — the satisfying bottom-out sound enthusiasts chase.",
      specs: ["Mechanical", "QMK"]
    }
  },

  mouse: {
    h: {
      name: "Mouse",
      one: "Pointing device that turns hand motion into cursor motion.",
      detail: "An optical sensor images the surface thousands of times per second and compares frames to measure movement — then sends deltas to the PC. DPI is sensitivity: how many cursor pixels per inch of movement. Wireless mice use 2.4 GHz dongles or Bluetooth.",
      fun: "The first mouse (1968, Douglas Engelbart) was a wooden block with two metal wheels.",
      specs: ["Optical sensor", "800–3200 DPI"]
    },
    c: {
      name: "Mouse — Sensors & Polling",
      one: "CPI, polling rates and why pros argue about 8 kHz.",
      detail: "Gaming mice push 26,000 CPI sensors and 8,000 Hz polling — the PC asks the mouse for position 8,000 times per second. Beyond 1 kHz the returns diminish, but latency-obsessed players buy it anyway. Wireless latency now rivals wired.",
      fun: "Sensor chips image the desk at 10,000+ frames per second — your mouse is a tiny high-speed camera.",
      specs: ["26K CPI", "1000 Hz"]
    }
  },

  speakers: {
    c: {
      name: "Speakers",
      one: "Turn electrical signals into sound waves.",
      detail: "Digital audio is converted to analog (DAC), amplified, and drives a voice coil in a magnetic field. The coil pushes a cone that moves air — that moving air is the sound wave. Frequency response describes how evenly it reproduces bass to treble.",
      fun: "Speakers and microphones are exact opposites: one turns electricity into motion, the other turns motion into electricity.",
      specs: ["2.0 stereo", "50 Hz – 20 kHz"]
    }
  },

  webcam: {
    c: {
      name: "Webcam",
      one: "Captures video for calls, classes and streaming.",
      detail: "A small CMOS image sensor records frames through a lens; USB webcams compress the video (MJPEG/H.264) before sending it to the PC. Sensor size and lens quality matter more than megapixels for image quality.",
      fun: "The first webcam (1991, Cambridge) watched a coffee pot, so researchers could check if there was coffee before walking over.",
      specs: ["1080p", "USB 2.0"]
    }
  },

  /* ---------- Tinkerer: motherboard-level ---------- */

  pcb: {
    t: {
      name: "PCB (Printed Circuit Board)",
      one: "Fiberglass laminate with copper traces — the canvas everything lives on.",
      detail: "PCBs are made of FR-4 fiberglass laminate with layers of copper foil. Traces are etched, then sealed under solder mask (the green coating) with silkscreen labels printed on top. A motherboard is typically 6–10 layers, with solid power and ground planes sandwiched inside.",
      fun: "A motherboard PCB starts as a copper-clad panel bigger than a door, then gets etched, drilled, plated and cut into shape.",
      specs: ["FR-4", "8 layers"]
    }
  },

  ios: {
    t: {
      name: "I/O Shield & Rear Ports",
      one: "USB, video, audio and network ports on the back panel.",
      detail: "The shield grounds the port cluster and lines up with the case cutout. Each port connects to a controller on the board: USB ports to the chipset's USB controllers, display outputs to the integrated GPU, audio jacks to the codec, Ethernet to the NIC.",
      fun: "Forgetting the I/O shield is the #1 classic build mistake — it only fits from the inside, so you notice after everything's screwed in.",
      specs: ["USB 3.2", "HDMI", "2.5G LAN"]
    }
  },

  socket: {
    t: {
      name: "CPU Socket (LGA1700)",
      one: "1,700 spring contacts connecting the CPU to the board.",
      detail: "In an LGA (Land Grid Array) socket the pins live in the socket, not the CPU. The retention arm clamps the CPU with even pressure so every pad makes contact. Older AMD sockets (PGA) had pins on the CPU itself — easy to bend, heartbreaking to fix.",
      fun: "The LGA1700 retention mechanism presses down with several kilograms of force to keep 1,700 contacts seated.",
      specs: ["LGA1700", "1700 pins"]
    }
  },

  "vrm-mos": {
    t: {
      name: "VRM — MOSFETs",
      one: "High-speed switches that chop 12 V into pulses.",
      detail: "The VRM (Voltage Regulator Module) turns 12 V into ~1.2 V for the CPU. MOSFETs act as switches, toggling hundreds of thousands of times per second; the on/off duty cycle sets the average output voltage. Modern boards use DrMOS — driver and MOSFETs integrated in one package.",
      fun: "CPU power stages switch at 300 kHz or more — each 'pulse' lasts about 3 microseconds.",
      specs: ["DrMOS", "~50 A/phase"]
    }
  },

  "vrm-choke": {
    t: {
      name: "VRM — Chokes (Inductors)",
      one: "Store energy in a magnetic field and smooth the current.",
      detail: "When the MOSFET switches on, current builds a magnetic field in the choke; when it switches off, the collapsing field keeps pushing current. The choke turns the choppy pulses into smooth, steady current — magnetic momentum, essentially.",
      fun: "A choke is just a coil of wire around a magnetic core — the same physics as a water-hammer arrestor in plumbing.",
      specs: ["Ferrite core", "~1 µH"]
    }
  },

  "vrm-cap": {
    t: {
      name: "VRM — Capacitors",
      one: "Tiny charge reservoirs that flatten voltage ripple.",
      detail: "Capacitors store and release charge to smooth the small ripple left after the choke. Solid polymer caps (the little cylinders) have low ESR and long life, and they also decouple high-frequency noise right next to the CPU.",
      fun: "Ripple after the full VRM chain is typically a few millivolts — cleaner than many lab bench power supplies.",
      specs: ["Solid polymer", "Low ESR"]
    }
  },

  dimm: {
    t: {
      name: "DIMM Slots",
      one: "Edge connectors with 288 pins per DDR5 slot.",
      detail: "DIMM slots grip the module's gold edge contacts. Two slots usually form one memory channel — populate the right pair for dual-channel bandwidth. The key notch sits in a different position for each DDR generation so the wrong RAM physically can't fit.",
      fun: "DDR4 and DDR5 both have 288 pins, but the notch moved — the slot knows the difference even if you don't.",
      specs: ["288 pins", "2 channels"]
    }
  },

  chipset: {
    t: {
      name: "Chipset (PCH)",
      one: "The traffic hub: USB, SATA, LAN and peripheral PCIe.",
      detail: "The Platform Controller Hub links the CPU to most peripherals — USB, SATA, Ethernet, audio and extra PCIe lanes — over a DMI link (about PCIe 4.0 x8 of bandwidth). The CPU itself keeps the fast lanes for RAM, the GPU and one M.2 slot.",
      fun: "Intel moved the memory controller into the CPU in 2009, shrinking the old 'northbridge' — the chipset is the surviving part.",
      specs: ["DMI 4.0 x8"]
    }
  },

  bios: {
    t: {
      name: "BIOS/UEFI Flash Chip (SPI ROM)",
      one: "The first program your computer runs.",
      detail: "This SPI flash chip stores the firmware (UEFI). At power-on the CPU executes it: it initializes hardware, trains memory, enumerates devices, then hands off to the OS bootloader. It's writable in place — that's how BIOS updates work.",
      fun: "If this chip's contents get corrupted the board won't boot — many boards have 'BIOS flashback' to reflash without a CPU installed.",
      specs: ["32 MB SPI", "UEFI"]
    }
  },

  crystal: {
    t: {
      name: "Crystal Oscillator",
      one: "The heartbeat that keeps every clock in sync.",
      detail: "A quartz crystal vibrates at a precise frequency (often 32.768 kHz for the real-time clock, or 25 MHz as a PCIe reference). The board multiplies this reference up to the GHz clocks the CPU and buses run on. Quartz is used because it's piezoelectric — electricity makes it physically vibrate, and it vibrates at one stubborn frequency.",
      fun: "32,768 Hz = 2^15. Divide it by two, fifteen times in a row, and you get exactly one tick per second — the clock's clock.",
      specs: ["32.768 kHz"]
    }
  },

  cmos: {
    t: {
      name: "CMOS Battery (CR2032)",
      one: "Keeps settings and the clock alive while the PC is off.",
      detail: "A 3 V lithium coin cell powers the real-time clock and preserves BIOS settings in a tiny SRAM when the system is unplugged. 'Clear CMOS' = reset those settings to defaults (usually a jumper or button).",
      fun: "The CR2032 is the same battery used in car key fobs — it can easily outlive the motherboard it sits on.",
      specs: ["CR2032", "3 V"]
    }
  },

  m2slot: {
    t: {
      name: "M.2 Slot (Key M)",
      one: "Direct PCIe/NVMe connector on the board.",
      detail: "Key M slots carry 4 PCIe lanes for NVMe SSDs; Key E slots are for Wi-Fi cards. The module lies flat and is secured by a single screw — which is tiny and loves to vanish into the carpet.",
      fun: "M.2 sizes like '2280' mean 22 mm wide and 80 mm long. The screw you just lost is an M2 × 3 mm.",
      specs: ["Key M", "PCIe 4.0 x4"]
    }
  },

  headers: {
    t: {
      name: "Headers (USB, Fan, Front Panel)",
      one: "Pin headers connecting the board to the outside world.",
      detail: "Headers are simple 0.1″ pin grids: USB 2.0 (9 pins), USB 3.0 (19 pins), 4-pin PWM fan headers (power, ground, tachometer, PWM control), RGB headers, and the front-panel pins. Pinout and polarity matter — headers are where the schematic meets the real world.",
      fun: "A PWM fan header both powers the fan and reads its RPM — the tach wire reports back every revolution.",
      specs: ["0.1″ pitch"]
    }
  },

  audio: {
    t: {
      name: "Audio Codec Chip",
      one: "ADC and DAC — converts between analog sound and digital audio.",
      detail: "The codec digitizes microphone input (ADC) and converts digital audio to analog for headphones (DAC), sampling at 44.1–192 kHz. Premium boards add headphone amplifiers, and isolate the audio section on the PCB to reduce digital noise.",
      fun: "CD-quality 44.1 kHz means the waveform is measured 44,100 times per second — twice the highest pitch you can hear.",
      specs: ["192 kHz DAC"]
    }
  },

  lan: {
    t: {
      name: "Ethernet Controller (PHY + MAC)",
      one: "The chip that speaks gigabit networking.",
      detail: "The MAC layer builds and checks frames; the PHY converts them into electrical signals on the cable, fighting noise, echo and attenuation with DSP. 2.5G/10G controllers do heavy signal processing over the same cheap copper.",
      fun: "Gigabit Ethernet pushes ~125 million symbols per second, bidirectionally, over all four wire pairs at once.",
      specs: ["2.5 GbE"]
    }
  },

  pcie: {
    t: {
      name: "PCIe Slots",
      one: "High-speed serial lanes for expansion cards.",
      detail: "PCIe is point-to-point: each lane is a differential pair (two wires with opposite polarity) in each direction. An x16 slot gives a GPU 16 lanes; x1 slots serve Wi-Fi and sound cards. Gen 4 moves ~2 GB/s per lane; Gen 5 doubles it.",
      fun: "PCIe traces must be length-matched to fractions of a millimetre — at these speeds, a 1 mm detour measurably skews the signal.",
      specs: ["x16 + 2×x1", "Gen 4"]
    }
  }
};
