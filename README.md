# VAVE Matrix Controller

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)
![License](https://img.shields.io/badge/license-proprietary-red.svg)

An enterprise-grade web application for managing and routing Video over IP (AV over IP) infrastructure using VAVE AVIP-H265 Matrix Switchers. The system communicates directly with the VAVE Control Server (AVIP-H265-1G-CTL) via HTTP APIs to automatically synchronize network endpoints, execute seamless video routing, and provide centralized AV management across multiple zones.

Developed by **SD PLUS GROUP CO.,LTD. | Bangkok, Thailand**

---

## ✨ Current Features (v1.0)

| Feature | Description |
|---|---|
| 🔄 **Auto-Sync Devices** | Automatically discovers and fetches all active encoders and decoders from the VAVE Control Server in real-time. Zero manual configuration required. |
| 🖱️ **Drag & Drop Routing** | Intuitive matrix switching — drag an input source and drop it onto one or more output displays to route video instantly. |
| ☑️ **Multi-Select Output** | Select multiple decoder outputs simultaneously and apply a single input source to all selected displays with one click. |
| 🌐 **VLAN Architecture** | Production-ready network design — Control traffic on VLAN 10 (`192.168.2.x`), AV streaming on VLAN 1 (`193.168.0.x`). |
| 🎨 **Modern UI** | Glassmorphism design with smooth animations, dark theme, and responsive layout built with HTML5, CSS3, and Vanilla JS. |
| 🚀 **Lightweight Backend** | Flask-based Python server with minimal dependencies. Deployable on any Windows or Linux machine. |

---

## 🗺️ Roadmap

### v1.1 — Routing Preset Templates
> Save and recall custom routing configurations with a single click.

- 📋 **Custom Presets**: Users can save the current input → output routing state as a named template (e.g., "Meeting Mode", "Presentation Mode", "All Screens HDMI1").
- ⚡ **One-Click Recall**: Apply any saved preset instantly — all outputs switch simultaneously according to the template mapping.
- 📦 **Import / Export**: Share preset configurations across multiple sites as JSON files.
- 🔒 **Lock Presets**: Admin-only presets that operators cannot modify.

### v1.2 — Multi-Source Multiview
> Display multiple video sources on a single screen simultaneously.

- 🖥️ **Picture-in-Picture (PiP)**: Overlay a secondary source on top of the primary output.
- 📐 **Quad-View / Grid Layout**: Split a single decoder output into 2×2 or custom grid layouts, each cell showing a different encoder source.
- 🎚️ **Per-Cell Source Assignment**: Drag and drop individual sources into specific cells of the multiview layout.
- 🔊 **Audio Follow**: Configure which source's audio is active in a multiview scenario.

### v1.3 — Display Layout Manager
> Visually design and manage complex display wall configurations.

- 🧩 **Visual Layout Editor**: Drag-and-drop canvas to arrange physical screen positions (e.g., 2×2 video wall, L-shaped layouts, asymmetric configurations).
- 📏 **Bezel Compensation**: Adjust for physical monitor bezels to ensure seamless content across tiled displays.
- 🗂️ **Zone Management**: Group outputs into named zones (e.g., "Lobby Wall", "Control Room", "Conference A") and apply routing per zone.
- 📱 **Responsive Preview**: Live thumbnail preview of all display outputs with real-time status indicators.

### v2.0 — Enterprise Features *(Planned)*
- 🔐 **User Authentication & Roles**: Admin, Operator, and Viewer roles with permission-based access control.
- 📊 **Dashboard & Analytics**: Real-time system health monitoring, device uptime tracking, and event logging.
- 🔗 **Multi-Controller Support**: Manage multiple VAVE Control Servers from a single unified interface.
- 📡 **Webhook & Automation**: Trigger routing changes via external events (scheduling, sensor input, third-party API).

---

## 🏗️ Architecture & Integration

```
┌─────────────────────────────────────────────────────────────┐
│                     VLAN 10 (Control)                       │
│                                                             │
│   ┌──────────────┐         ┌──────────────────────────┐     │
│   │  Web Browser  │ ◄────► │  Python Flask Server     │     │
│   │  (User UI)    │  HTTP  │  (localhost:5000)         │     │
│   └──────────────┘         └────────┬─────────────────┘     │
│                                     │ HTTP API               │
│                            ┌────────▼─────────────────┐     │
│                            │  VAVE Control Server     │     │
│                            │  AVIP-H265-1G-CTL        │     │
│                            │  192.168.2.10            │     │
│                            └────────┬─────────────────┘     │
└─────────────────────────────────────┼───────────────────────┘
                                      │
┌─────────────────────────────────────┼───────────────────────┐
│                     VLAN 1 (AV Data)│                       │
│                                     │                       │
│   ┌──────────┐    ┌──────────┐    ┌─▼────────┐              │
│   │ Encoder 1│    │ Encoder 2│    │ Decoder 1│ ─► Display 1 │
│   │ (TX)     │    │ (TX)     │    │ (RX)     │              │
│   │ HDMI1    │    │ Wireless │    │ TV1      │              │
│   └──────────┘    └──────────┘    └──────────┘              │
│                                   ┌──────────┐              │
│                                   │ Decoder 2│ ─► Display 2 │
│                                   │ (RX)     │              │
│                                   │ TV2      │              │
│                                   └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

**API Endpoints (VAVE Control Server)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/cgi-bin/getjson.cgi?json=mxsta` | Fetch all device status (encoders, decoders, system info) |
| `GET` | `/cgi-bin/submit?cmd=SET DEC {id} SWITCH {id} ALL USER admin` | Route encoder to decoder |
| `GET` | `/cgi-bin/capture.cgi?hostip={ip}&capwidth=240` | Capture preview thumbnail from encoder |

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd vave-matrix-controller
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   # Or double-click run_metrix.bat on Windows
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

> **Note:** The machine running this application must have network access to the VAVE Control Server on VLAN 10 (`192.168.2.10`).

## 📋 Requirements

| Dependency | Version |
|------------|---------|
| Python | 3.8+ |
| Flask | Latest |
| Requests | Latest |
| Network | Access to VAVE Control Server (`192.168.2.10`) |

## 📄 License

Proprietary software. All rights reserved.  
Developed and maintained by **SD PLUS GROUP CO.,LTD.** — Bangkok, Thailand.  
Unauthorized reproduction or distribution is strictly prohibited.
