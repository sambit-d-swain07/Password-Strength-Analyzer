# 🔒 Cryptographic Password Strength Analyzer & Security Auditor

A high-fidelity, desktop-based cybersecurity utility designed to evaluate password entropy, prevent credential reuse, and generate cryptographically secure alternatives. Built with a premium, hardware-inspired "anti-gravity" dark mode interface and backed by strict zero-plaintext storage protocols.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-cyan.svg)
![Security](https://img.shields.io/badge/security-CSPRNG%20%7C%20Bcrypt-brightgreen.svg)

---

## ⚡ Key Features

### 🎨 Premium UI/UX & Aesthetic
*   **Anti-Gravity Glassmorphism:** A floating, minimalist control card with sharp 1px borders and deep multi-layered drop shadows.
*   **Real-Time Telemetry Gauge:** A dynamic, segmented progress indicator that shifts gracefully from Crimson Red (Critical Vulnerability) to Tactical Emerald Green (Cryptographically Secure).
*   **Terminal-Style Diagnostics:** Clean, scannable security feedback headers (`✓ ENTROPY CHECK PASSED`, `⚠ SEQUENTIAL PATTERN DETECTED`).
*   **High-Entropy Generator:** One-click secure credential generation with automated clipboard mapping and non-intrusive toast notifications.

### 🧠 Technical Security Architecture
*   **Comprehensive Assessment Engine:** Measures bit-length (12–16+ characters), mixed-case distribution, numerical density, and non-alphanumeric special character arrays.
*   **Algorithmic Pattern Filtering:** Actively scans for and flags predictable dictionary terms, keyboard walks (`qwerty`, `asdf`), and sequential sequences (`123456`).
*   **CSPRNG Engine:** Utilizes true cryptographically secure pseudo-random number generation via Python's `secrets` module to ensure unpredictable structures.

### 💾 Anti-Reuse Protocol (Zero-Plaintext Database)
*   **Lightweight Storage Architecture:** Integrated local SQLite schema managing a historic `password_history` ledger.
*   **Salted Hashing Pipeline:** Implements a strict zero-plaintext rule. Passwords are immediately salted and processed using one-way cryptographic hashing (`bcrypt`) before archiving.
*   **Duplication Diagnostics:** Real-time lookup routine blocks historical matching, raising an immediate archive conflict warning state if an identical footprint is detected.

---

## 🛠️ Core Cryptographic Concepts Applied

This project serves as a practical implementation of fundamental cybersecurity and cryptographic primitives:
1.  **Password Entropy:** Maximizing the algorithmic problem space to render brute-force and dictionary attacks computationally infeasible.
2.  **One-Way Cryptographic Hashing:** Utilizing hashing algorithms where processing input into a digest is efficient, but reverse-engineering the digest to discover the plaintext is mathematically impossible.
3.  **Unique Salting:** Appending unique, secure random strings to inputs prior to hashing to completely neutralize precomputed rainbow table attacks.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10 or higher
*   Pip package manager

### Installation & Setup

Install required dependencies:

Bash
pip install -r requirements.txt

Initialize and run the application:

Bash
python main.py

├── main.py              # Application entry point & UI Router
├── core/
│   ├── __init__.py
│   ├── evaluator.py     # Entropy calculation & pattern scanning engine
│   └── generator.py     # CSPRNG secure password string factory
├── database/
│   ├── __init__.py
│   ├── db_manager.py    # SQLite local schema configuration
│   └── security.py     # Bcrypt salting & cryptographic hashing pipeline
├── gui/
│   └── dashboard.py     # CustomTkinter modern UI rendering layout
└── README.md

