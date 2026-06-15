# 🌱 EcoHarvest AI — Sustainable Agriculture Optimization & Resource Management

> An AI-powered agricultural assistant that empowers farmers with personalized, real-time recommendations for crop selection, cost management, and pest detection.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Modules](#modules)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Future Scope](#future-scope)
- [References](#references)

---

## Overview

Agriculture remains a cornerstone of the global economy, yet farmers face mounting challenges — unpredictable weather, rising input costs, pest outbreaks, and a lack of actionable, data-driven guidance. Existing tools are fragmented, reactive, and generalized.

**EcoHarvest AI** is an end-to-end, AI-powered agricultural assistant built with **Streamlit**, **LangChain**, and **Groq LLMs** (llama3-70b). It integrates real-time weather data, AI-driven reasoning, and computer vision into a single, farmer-friendly platform, transforming complex agricultural decisions into clear, personalized, and sustainable recommendations.

---

## Features

- 🌾 **Crop Recommendation** — Location-aware, weather-driven crop suggestions with ranked priorities and risk analysis
- 💰 **Cost & Yield Optimization** — Short-term (3–6 months) and long-term (1–3 years) resource management strategies
- 🔬 **Pest & Disease Detection** — CNN-assisted image analysis and symptom-based LLM diagnosis with dual treatment plans
- 🔐 **Secure Authentication** — Session-based login to protect access and personalize the experience
- 🕓 **Session History** — Revisit past queries and recommendations within the same session
- 📋 **Markdown Output** — Clean, readable results formatted for farmers and agronomists alike

---

## System Architecture

```
User
 └─► Streamlit Frontend
       └─► Authentication Module
             └─► Feature Modules (Crop / Cost / Pest)
                   └─► LangChain Reasoning Engine
                         ├─► Groq LLM API (llama3-70b)
                         └─► OpenWeatherMap API
                               └─► AI-Driven Output → Streamlit Display
```

**Data Flow:**
`User Input (Location / Image / Symptoms)` → `Fetch Real-Time Weather` → `LangChain Prompt Template` → `Groq LLM Reasoning` → `Structured Markdown Output` → `Session History Storage` → `Streamlit Display`

---

## Modules

### 1. 🔐 Authentication Module
Implements a secure session-based login system using Streamlit session state. Users authenticate with a username and password before accessing any feature. A logout option prevents unauthorized continued access.

### 2. 🌾 Crop Recommendation Module
Fetches real-time weather data via the **OpenWeatherMap API**, then passes location, season, and climate parameters through a **LangChain prompt** to the **Groq LLM**. Returns 3–5 ranked crop suggestions with planting tips, soil guidance, and potential risk factors.

**Example:** Location: Vijayawada, India | Month: June → *Paddy, Maize, Cotton* with soil and irrigation guidelines.

### 3. 💰 Cost & Yield Optimization Module
Generates a personalized farm management plan using LLM reasoning over user-supplied farm parameters (acreage, crop type, resources). Delivers:
- **Short-term:** Irrigation scheduling, fertilizer optimization, SRI techniques
- **Long-term:** Drip irrigation investment, crop rotation, machinery planning

**Example:** 10-acre paddy farmer → Short-term irrigation scheduling + long-term drip investment plan.

### 4. 🔬 Pest & Disease Detection Module
Accepts either an **uploaded leaf image** (CNN placeholder for classification) or a **text description of symptoms**. The LLM synthesizes a diagnosis and produces a dual treatment plan covering organic, chemical, and preventive measures.

**Example:** White spots on uploaded leaf image → *Powdery Mildew* diagnosis + Neem oil spray, spacing recommendations, sanitation protocol.

### 5. 🕓 Session History Management
All queries and AI responses are stored in Streamlit's session state, allowing farmers to scroll through and revisit previous recommendations within their active session.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Reasoning | LangChain + Groq LLM (llama3-70b) |
| Image Analysis | CNN Placeholder (Pillow) |
| Weather Data | OpenWeatherMap API |
| Language | Python 3.10+ |
| Environment | Virtualenv / Conda |
| Version Control | Git & GitHub |

---

## Requirements

**Hardware:**
- 8 GB RAM minimum (GPU recommended for CNN training)
- 4-core CPU
- 2 GB storage for application and datasets

**Software:**
- Python 3.10+
- Windows, Linux, or macOS

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ecoharvest-ai.git
   cd ecoharvest-ai
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**

   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Open your browser at `http://localhost:8501`
2. Log in with your credentials
3. Select a module from the sidebar:
   - **Crop Recommendation** — Enter your location and the current month
   - **Cost & Yield Optimization** — Input farm size, crop type, and available resources
   - **Pest & Disease Detection** — Upload a leaf image or describe symptoms in text
4. Review the AI-generated recommendations and download or revisit them from session history

---

## Results

Sample outputs demonstrating real-world applicability:

| Module | Sample Input | Output |
|---|---|---|
| Crop Recommendation | Vijayawada, India — June | Paddy, Maize, Cotton ranked with risk analysis |
| Cost & Yield | 10-acre paddy farm | SRI method (short-term) + drip irrigation investment (long-term) |
| Pest Detection | Leaf image with white spots | Powdery Mildew — Neem oil (organic) + fungicide (chemical) |

All outputs are rendered in **Markdown format** for clarity and farmer readability.

---

## Future Scope

| Priority | Feature |
|---|---|
| 🔴 High | Full CNN integration using PlantVillage datasets for accurate disease classification |
| 🟠 Medium | IoT sensor integration for real-time soil health and NPK monitoring |
| 🟡 Medium | Market price forecasting using time-series models |
| 🟢 Low | Multilingual and offline support for rural accessibility |

---

## References

This project draws on research in sustainable and precision agriculture:

- Konfo et al. (2024) — Climate-smart innovations in agrifood systems
- Greco et al. (2020) — Biowaste valorisation in circular bioeconomy
- Choruma et al. (2024) — Digitalisation challenges for smallholder farmers in Sub-Saharan Africa
- Rakholia et al. (2024) — Technology adoption for sustainable agriculture in India
- Kwaghtyo & Eke (2023) — AI prediction models for precision agriculture
- Rajak et al. (2023) — IoT and smart sensors in agriculture
- Rodríguez et al. (2021) — IoT-Agro smart farming system
- Lykas & Vagelas (2023) — Innovations for sustainable agro-systems

---

## Keywords

`EcoHarvest AI` · `Sustainable Agriculture` · `Crop Recommendation` · `Cost & Yield Optimization` · `Pest & Disease Detection` · `Precision Farming` · `LangChain` · `Groq LLM` · `Streamlit` · `AI-driven Farming`

---

> *"AI can revolutionize agriculture — making farming more resilient, data-driven, and sustainable."*
