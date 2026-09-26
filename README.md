# 🏔️ Weekend Trip Planner — Nepal

An AI-powered trip planner for Nepal built with **Streamlit** and the **Groq API**.

Describe the kind of trip you want, select your destinations, and an AI agent generates a day-by-day itinerary for each city using live weather, nearby hotels and restaurants, driving distances, and destination information.

The project started as a classroom exercise on building AI agents from scratch using a **think–act–observe loop with tools and shared state**, without relying on an agent framework. It was then developed into a deployable web application.

## 🚀 Live Demo

[![Open Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-00A67E?style=for-the-badge)](https://weekend-trip-planner-qqrjysyvi8aztxaljcmwz6.streamlit.app/)

👉 **Try the deployed application:**
[https://weekend-trip-planner-qqrjysyvi8aztxaljcmwz6.streamlit.app/]

---

## ✨ Features

### 🗺️ Multi-City AI Itineraries

Choose one or more destinations from:

* 🏔️ Pokhara
* 🏛️ Kathmandu
* 🛕 Lumbini
* ⛰️ Manang
* 🏞️ Mustang

Specify the number of days for each destination and describe your preferred travel style in natural language.

### 🤖 Agent-Built Travel Plans

Each selected city receives its own agent run.

The agent can:

* Find suitable activities
* Add activities to the itinerary
* Remove activities when necessary
* Manage the available days
* Automatically fill remaining time

The agent operates through a bounded **think–act–observe loop** rather than an unrestricted process.

### 🌤️ Live Travel Data

The application retrieves travel information at request time from multiple external APIs:

| Data                              | Source                     |
| --------------------------------- | -------------------------- |
| 🌤️ Weather & 3-day forecast      | Open-Meteo                 |
| 🏨 Hotels & 🍽️ Restaurants       | OpenStreetMap Overpass API |
| 🚗 Driving distances              | OSRM                       |
| 🖼️ Destination & activity images | Wikipedia REST API         |

### 📊 Per-City Results

Each destination provides dedicated sections for:

* 🗓️ Itinerary
* 🌤️ Weather
* 🏨 Stay & Eat
* 📋 Trip Summary
* 📈 Progress
* 🔍 Agent Log

The **Agent Log** displays the tool calls made during itinerary generation, making the agent's actions more transparent.

### 📄 Export

The complete itinerary can be exported as:

* PDF
* Text

PDF generation is handled using **ReportLab**.

### 🛡️ Cost & Abuse Guardrails

The application includes limits to control API usage:

* Maximum agent steps per city
* Maximum total agent steps per trip
* Maximum generations per browser session

These limits help keep API usage predictable and prevent excessive requests.

### 🎨 Custom Interface

The application includes a custom-themed Streamlit interface with:

* Dusk/marigold visual theme
* Fraunces typography
* IBM Plex typography
* Interactive destination selection
* Per-city result tabs

---

## 🧠 How the AI Agent Works

Each selected city receives an independent agent run.

### Step 1 — User Input

The user provides:

* Selected destinations
* Number of days for each destination
* Preferred travel style
* Trip preferences

### Step 2 — Agent Initialization

The agent receives:

* A goal-oriented system prompt
* The available day budget
* The user's preferences
* A live weather summary
* The selected city's information

### Step 3 — Tool Selection

The agent can call three tools:

```text
find_activities
add_to_itinerary
remove_from_itinerary
```

These tools interact with a shared state containing information such as:

```text
days_remaining
itinerary
```

### Step 4 — Think–Act–Observe Loop

The agent operates through a bounded loop:

```text
Think
  ↓
Choose a tool
  ↓
Execute the tool
  ↓
Observe the result
  ↓
Update trip state
  ↓
Repeat
```

The loop continues until the itinerary is complete or the configured step limit is reached.

### Step 5 — Automatic Completion

If the agent reaches its step limit while some time remains, the application automatically fills the remaining itinerary slots.

### Step 6 — Transparent Agent Log

Each tool call is recorded and displayed in the application's **Agent Log**, allowing users to see how the itinerary was constructed.

---

## 🧩 AI Model

The application uses:

**Model:** `openai/gpt-oss-20b`
**Inference Provider:** Groq API

The model is used to generate and manage the travel itinerary through the custom tool-calling agent loop.

---

## 🏗️ Architecture

The application follows a simple tool-based agent architecture:

```text
                    ┌─────────────────────┐
                    │       User          │
                    │ Destinations +      │
                    │ Travel Preferences  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit App     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     AI Agent        │
                    │  Groq + LLM Model   │
                    └──────────┬──────────┘
                               │
                  ┌────────────┼────────────┐
                  │            │            │
                  ▼            ▼            ▼
          find_activities  add_to_itinerary  remove_from_itinerary
                  │            │            │
                  └────────────┼────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Shared Trip State │
                    │ itinerary           │
                    │ days_remaining      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Final Itinerary   │
                    └─────────────────────┘
```

---

## 🌐 External Data Sources

The application integrates several external services.

### Open-Meteo

Used for:

* Current weather information
* 3-day weather outlook

[Open-Meteo](https://open-meteo.com/)

### OpenStreetMap Overpass API

Used to retrieve nearby:

* Hotels
* Restaurants

[OpenStreetMap Overpass API](https://overpass-api.de/)

### OSRM

Used for:

* Driving-distance calculations

[OSRM](http://project-osrm.org/)

### Wikipedia REST API

Used for:

* Destination information
* Activity and destination images

[Wikipedia REST API](https://www.mediawiki.org/wiki/API:REST_API)

---

## 🛠️ Tech Stack

### Application

* Python
* Streamlit

### AI

* Groq API
* `openai/gpt-oss-20b`
* Custom tool-calling agent
* Think–Act–Observe loop

### APIs & Data

* Open-Meteo
* OpenStreetMap Overpass API
* OSRM
* Wikipedia REST API

### Export

* ReportLab

### Deployment

* Streamlit Community Cloud

---

## 📁 Project Structure

```text
weekend-trip-planner/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

### File Description

| File                      | Purpose                                                                             |
| ------------------------- | ----------------------------------------------------------------------------------- |
| `app.py`                  | Main Streamlit application, UI, agent loop, tools, API integrations, and PDF export |
| `requirements.txt`        | Python dependencies                                                                 |
| `.gitignore`              | Prevents sensitive/unnecessary files from being committed                           |
| `.streamlit/secrets.toml` | Stores the Groq API key locally                                                     |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/DeepakChaudhary369/weekend-trip-planner.git
cd weekend-trip-planner
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Groq API Key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

> ⚠️ Never commit `secrets.toml` to GitHub. Keep API keys private and rotate them immediately if they are accidentally exposed.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## ☁️ Deployment on Streamlit Community Cloud

To deploy the application:

### 1. Push the repository to GitHub

Make sure your API key is **not** committed.

### 2. Open Streamlit Community Cloud

Create a new application and select this GitHub repository.

### 3. Select the main file

Use:

```text
app.py
```

### 4. Configure Secrets

In the Streamlit application's settings, add:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

### 5. Deploy

Streamlit Community Cloud will install the dependencies from:

```text
requirements.txt
```

and launch the application.

---

## 🛡️ Security

The Groq API key is stored using Streamlit secrets.

Local secrets are stored in:

```text
.streamlit/secrets.toml
```

and should never be committed to the repository.

The project includes `.gitignore` rules to prevent the secrets file from being uploaded accidentally.

If an API key is ever exposed publicly:

1. Revoke the exposed key.
2. Generate a new key.
3. Update the Streamlit secret.
4. Check Git history if the key was committed previously.

---

## ⚙️ Agent Guardrails

The application intentionally limits agent execution.

The main controls include:

```text
STEP_BUDGET_CAP_PER_CITY
MAX_TOTAL_AGENT_STEPS_PER_TRIP
MAX_GENERATIONS_PER_SESSION
```

These limits help:

* Control API usage
* Prevent excessive agent loops
* Reduce accidental cost
* Improve application reliability

---

## 📌 Current Limitations

The current application supports five predefined destinations:

* Pokhara
* Kathmandu
* Lumbini
* Manang
* Mustang

Adding a new destination requires updating the corresponding city/activity configuration in `app.py`.

The application also depends on external APIs for weather, maps, places, routing, images, and LLM inference. Availability and response quality may therefore depend on those external services.

---

## 🔮 Future Improvements

Potential future improvements include:

* Expanding the list of supported destinations
* Adding hotel and restaurant ratings
* Adding estimated trip budgets
* Adding transportation options
* Adding map-based itinerary visualization
* Adding user authentication and saved trips
* Adding multilingual itinerary generation
* Improving activity ranking and personalization
* Adding real-time travel alerts
* Integrating additional travel data sources

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Generative AI
* AI agents
* Tool calling
* Shared agent state
* LLM application development
* API integration
* Streamlit application development
* External data retrieval
* Interactive UI design
* PDF generation
* API cost guardrails
* Cloud deployment

---

## 👨‍💻 Author

**Deepak Chaudhary**

Computer Science & Engineering — Data Science

[GitHub](https://github.com/DeepakChaudhary369)

[LinkedIn](https://www.linkedin.com/in/deepakchaudhary369)
