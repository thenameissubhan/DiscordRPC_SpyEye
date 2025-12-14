
# SpyEye

> **SpyEye** — A Discord Rich Presence application that displays *authorized* system and gaming activity as rich status on Discord.  
> **Important:** Use ONLY on devices you own or administer and with explicit consent. This project is intended for personal use, streaming/game-status display, and development — not covert surveillance.

---

## Quick Overview

SpyEye focuses on powerful features and a seamless user experience for showing activity in Discord Rich Presence. It summarizes authorized application and gaming state and forwards *summarized* notifications to a remote endpoint you control (optional).

---

## The SpyEye Journey: A Quick Tour of V1, V2, and V3

### V1 — The Foundation
- **Two-Part System:** V1 shipped as a background executable (`SpyEye.exe`) plus a separate monitor console (`SpyEyeConsole.exe`) for local observation.
- **Basic Presence:** Provided Discord Rich Presence updates and simple activity icons.

### V2 — Enhanced and Streamlined
- **Single Executable:** Consolidated into one all-in-one executable (`SpyEye_v2.exe`) for easier deployment.
- **Advanced Logging:** Introduced structured logs: `spyeye_error.log` and `spyeye_usage.log`.
- **GPU Monitoring:** Detects active Steam games and reports GPU usage and GPU temperature (for diagnostics and streaming overlays).

### V3 — Real-Time & Connected
- **Remote Notifications (Optional):** Optional integration to send summarized activity logs to a messaging bot (e.g., Telegram) you control for remote personal monitoring or stream overlays.
- **Privacy-by-Design:** All remote features require explicit configuration and authentication.

---

## Features
- Discord Rich Presence integration for games and apps you authorize.
- Optional local logging for diagnostics (`spyeye_error.log`, `spyeye_usage.log`).
- GPU detection and telemetry for supported titles (useful for stream overlays).
- Optional remote webhook/bot forwarding for personal notifications (configurable).
- Small footprint, designed for personal/dev use and streaming setups.

---

## Screenshots — SpyEye V2 in Action

Below are example screenshots showing the UI and Discord presence. (Click to view full size.)

<p align="center">
  <a href="https://github.com/user-attachments/assets/5f5d05f4-e84f-4858-8c11-4e1ebb48950e">
    <img src="https://github.com/user-attachments/assets/5f5d05f4-e84f-4858-8c11-4e1ebb48950e" alt="screenshot1" width="300" style="margin:4px">
  </a>
  <a href="https://github.com/user-attachments/assets/19ce8c66-5dea-489a-804d-4556c0b3a0c6">
    <img src="https://github.com/user-attachments/assets/19ce8c66-5dea-489a-804d-4556c0b3a0c6" alt="screenshot2" width="300" style="margin:4px">
  </a>
  <a href="https://github.com/user-attachments/assets/97977248-aedd-47d4-ad19-5d10748161c3">
    <img src="https://github.com/user-attachments/assets/97977248-aedd-47d4-ad19-5d10748161c3" alt="screenshot3" width="300" style="margin:4px">
  </a>
</p>

<p align="center">
  <a href="https://github.com/user-attachments/assets/71252f82-6304-44c8-b632-898355726e78">
    <img src="https://github.com/user-attachments/assets/71252f82-6304-44c8-b632-898355726e78" alt="screenshot4" width="300" style="margin:4px">
  </a>
  <a href="https://github.com/user-attachments/assets/bc559886-d464-477c-9b93-522bfe58bab8">
    <img src="https://github.com/user-attachments/assets/bc559886-d464-477c-9b93-522bfe58bab8" alt="screenshot5" width="300" style="margin:4px">
  </a>
  <a href="https://github.com/user-attachments/assets/8ebf766d-6a14-4f3e-bf00-a8d924735afd">
    <img src="https://github.com/user-attachments/assets/8ebf766d-6a14-4f3e-bf00-a8d924735afd" alt="screenshot6" width="300" style="margin:4px">
  </a>
</p>

---

## Documentation
Full documentation:  
https://docs.google.com/document/d/1vz6IqZGzbNlSzr-i85gwsoK8gTwPYrjc3edw4he1Npw/edit?usp=sharing

---

## Privacy & Safety
- **Only run SpyEye on devices you own or are authorized to monitor.**
- **Do not use for covert monitoring.** Always obtain consent from users.
- Protect log files and any forwarded data. Use secure tokens for remote integrations.

---

