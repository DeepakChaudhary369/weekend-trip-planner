# 🏔️ Weekend Trip Planner — Nepal

An AI-powered trip planner for Nepal, built with **Streamlit** and the **Groq API**. Describe the kind of trip you want, pick your destinations, and an autonomous agent builds a day-by-day itinerary for each city — grounded in live weather, real hotels/restaurants, driving distances, and destination photos.

This app grew out of a classroom exercise on building AI agents from scratch (a think–act–observe loop with tools and shared state, no agent framework involved) and was turned into a deployable web app.

## ✨ Features

- **Multi-city agentic itineraries** — pick one or more of Pokhara, Kathmandu, Lumbini, Manang, and Mustang, set how many days per stop, and describe your travel style in plain language.
- **Agent-built plans** — for each city, an LLM agent calls tools (`find_activities`, `add_to_itinerary`, `remove_from_itinerary`) in a bounded think–act–observe loop to fill the available days, then auto-fills any leftover time.
- **Live travel data**, pulled at request time:
  - 🌤️ Weather & 3-day outlook — [Open-Meteo](https://open-meteo.com/)
  - 🏨🍽️ Nearby hotels & restaurants — [OpenStreetMap Overpass API](https://overpass-api.de/)
  - 🚗 Driving distances — [OSRM](http://project-osrm.org/)
  - 🖼️ Destination & activity photos — [Wikipedia REST API](https://www.mediawiki.org/wiki/API:REST_API)
- **Per-city results tabs** — itinerary, weather, stay & eat, trip summary (with progress bar), and a transparent agent log showing every tool call the agent made.
- **PDF & text export** of the full itinerary, generated with `reportlab`.
- **Built-in cost/abuse guardrails** — capped agent steps per city, capped total steps per trip, and a capped number of generations per browser session.
- Custom-themed UI (dusk/marigold palette, Fraunces + IBM Plex typefaces).

## 🧠 How the agent works

Each selected city gets its own agent run, scoped to that city only:

1. The agent is given a goal-oriented system prompt, the day budget, the traveler's stated preferences, and a live weather summary.
2. On each step it can call one of three tools — `find_activities`, `add_to_itinerary`, `remove_from_itinerary` — which read and write a shared per-city trip state (`days_remaining`, `itinerary`).
3. The loop runs until the agent finishes or hits its step cap (`STEP_BUDGET_CAP_PER_CITY`), after which any remaining time is auto-filled.
4. Every tool call is recorded and shown in the **Agent Log** tab, so the reasoning process is visible rather than a black box.

Model used: `openai/gpt-oss-20b` via the Groq API.

## 🚀 Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your Groq API key

Get a free API key from [console.groq.com](https://console.groq.com/), then create `.streamlit/secrets.toml` in the project root:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

> ⚠️ Never commit `secrets.toml` — it's already covered by `.gitignore`. If a key is ever exposed (e.g. pasted in a chat or committed by mistake), rotate it immediately in the Groq console.

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. On [share.streamlit.io](https://share.streamlit.io/), create a new app pointing to `app.py` on your repo.
3. In the app's **Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
4. Deploy — no other configuration needed.

## 📁 Project structure

```
.
├── app.py               # Main Streamlit app (UI, agent loop, tools, data integrations, PDF export)
├── requirements.txt      # Python dependencies
├── .gitignore
└── .streamlit/
    └── secrets.toml      # Local secrets (not committed) — holds GROQ_API_KEY
```

## 🛠️ Tech stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Groq](https://groq.com/) — LLM inference (`openai/gpt-oss-20b`)
- [Open-Meteo](https://open-meteo.com/), [Overpass API](https://overpass-api.de/), [OSRM](http://project-osrm.org/), [Wikipedia REST API](https://www.mediawiki.org/wiki/API:REST_API) — live travel data
- [ReportLab](https://www.reportlab.com/) — PDF generation

## 📌 Notes & limits

- Destinations are currently fixed to five Nepal locations (Pokhara, Kathmandu, Lumbini, Manang, Mustang); adding a new city means extending `ACTIVITIES`, `CITY_EMOJI`, `CITY_TAGLINES`, and the image title maps in `app.py`.
- Session guardrails (`STEP_BUDGET_CAP_PER_CITY`, `MAX_TOTAL_AGENT_STEPS_PER_TRIP`, `MAX_GENERATIONS_PER_SESSION`) exist to keep API costs bounded — adjust them in `app.py` if you need different limits.
