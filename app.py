import json
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Weekend Trip Planner",
    page_icon="✈️",
    layout="centered",
)


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL = "openai/gpt-oss-20b"


# ============================================================
# ACTIVITIES
# ============================================================

ACTIVITIES = {
    "Pokhara": [
        {
            "name": "Phewa Lake boating",
            "duration_days": 0.5,
        },
        {
            "name": "Sarangkot sunrise hike",
            "duration_days": 0.5,
        },
        {
            "name": "Annapurna foothills day hike",
            "duration_days": 1.0,
        },
        {
            "name": "World Peace Pagoda visit",
            "duration_days": 0.5,
        },
    ],
    "Kathmandu": [
        {
            "name": "Swayambhunath (Monkey Temple) visit",
            "duration_days": 0.5,
        },
        {
            "name": "Bhaktapur Durbar Square day trip",
            "duration_days": 1.0,
        },
        {
            "name": "Thamel food and shopping walk",
            "duration_days": 0.5,
        },
        {
            "name": "Nagarkot sunrise viewpoint",
            "duration_days": 1.0,
        },
    ],
}


# ============================================================
# SESSION STATE
# ============================================================

if "trip_state" not in st.session_state:
    st.session_state.trip_state = {
        "days_remaining": 0.0,
        "itinerary": [],
    }


def get_trip_state():
    return st.session_state.trip_state


# ============================================================
# ACTIVITY DURATIONS
# ============================================================

ACTIVITY_DURATIONS = {
    activity["name"]: activity["duration_days"]
    for options in ACTIVITIES.values()
    for activity in options
}


# ============================================================
# TOOL 1: FIND ACTIVITIES
# ============================================================

def find_activities(city: str) -> str:

    options = ACTIVITIES.get(city)

    if not options:
        return f"No activities on file for {city}."

    listed = [
        f"{activity['name']} ({activity['duration_days']} day(s))"
        for activity in options
    ]

    return f"Activities in {city}: " + "; ".join(listed)


# ============================================================
# TOOL 2: ADD TO ITINERARY
# ============================================================

def add_to_itinerary(activity: str) -> str:

    state = get_trip_state()

    duration = ACTIVITY_DURATIONS.get(activity)

    if duration is None:
        return (
            f"'{activity}' is not a known activity. "
            "Call find_activities first."
        )

    if duration > state["days_remaining"]:
        return (
            f"'{activity}' needs {duration} day(s), but only "
            f"{state['days_remaining']} day(s) remain. Not added."
        )

    state["itinerary"].append(activity)
    state["days_remaining"] -= duration

    return (
        f"Added '{activity}'. "
        f"Itinerary so far: {state['itinerary']}. "
        f"{state['days_remaining']} day(s) remaining."
    )


# ============================================================
# TOOL 3: REMOVE FROM ITINERARY
# ============================================================

def remove_from_itinerary(activity: str) -> str:

    state = get_trip_state()

    if activity not in state["itinerary"]:
        return f"'{activity}' is not currently in the itinerary."

    state["itinerary"].remove(activity)

    state["days_remaining"] += ACTIVITY_DURATIONS.get(
        activity,
        0,
    )

    return (
        f"Removed '{activity}'. "
        f"Itinerary now: {state['itinerary']}. "
        f"{state['days_remaining']} day(s) remaining."
    )


# ============================================================
# TOOL REGISTRY / WHITELIST
# ============================================================

REGISTRY = {
    "find_activities": find_activities,
    "add_to_itinerary": add_to_itinerary,
    "remove_from_itinerary": remove_from_itinerary,
}


# ============================================================
# TOOL SCHEMAS
# ============================================================

TOOL_SCHEMA = [

    {
        "type": "function",
        "function": {
            "name": "find_activities",
            "description": (
                "List the activities available in a city, "
                "with how many days each one takes. "
                "Use this before proposing anything to add."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Exact city name.",
                    }
                },
                "required": ["city"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "add_to_itinerary",
            "description": (
                "Add one activity to the trip itinerary. "
                "Only call this for an activity already found "
                "with find_activities. It will be rejected if "
                "it does not fit in the days remaining."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "activity": {
                        "type": "string",
                        "description": "Exact activity name.",
                    }
                },
                "required": ["activity"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "remove_from_itinerary",
            "description": (
                "Remove an activity that was already added "
                "to the itinerary and free its days."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "activity": {
                        "type": "string",
                        "description": "Exact activity name.",
                    }
                },
                "required": ["activity"],
            },
        },
    },
]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM = """
You are a weekend trip planning assistant.

Your job is to build a short itinerary using the available tools.

Rules:

1. Always call find_activities before adding activities.
2. Only add activities that exist in the tool result.
3. Check the remaining days before adding an activity.
4. Never exceed the user's requested number of days.
5. Do not repeat an activity unless the user explicitly asks.
6. If an activity does not fit, choose a smaller activity.
7. You may remove an activity if necessary to improve the itinerary.
8. Stop when the available trip time is full or a good itinerary
   has been created.
9. At the end, provide a clear and attractive itinerary.
"""


# ============================================================
# AGENT
# ============================================================

def run_agent(
    goal: str,
    total_days: float,
    max_steps: int = 8,
):

    # Reset state for this trip
    st.session_state.trip_state = {
        "days_remaining": total_days,
        "itinerary": [],
    }

    messages = [
        {
            "role": "system",
            "content": SYSTEM,
        },
        {
            "role": "user",
            "content": goal,
        },
    ]

    tool_log = []

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMA,
        )

        message = response.choices[0].message

        messages.append(
            message.model_dump(exclude_none=True)
        )

        # ----------------------------------------------------
        # FINAL ANSWER
        # ----------------------------------------------------

        if not message.tool_calls:

            return (
                message.content or "",
                tool_log,
            )

        # ----------------------------------------------------
        # TOOL EXECUTION
        # ----------------------------------------------------

        for call in message.tool_calls:

            name = call.function.name

            try:
                args = json.loads(
                    call.function.arguments or "{}"
                )
            except json.JSONDecodeError:

                result = (
                    "Error: invalid tool arguments."
                )

                tool_log.append(
                    f"Step {step}: {name} -> {result}"
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result,
                    }
                )

                continue

            # ------------------------------------------------
            # WHITELIST CHECK
            # ------------------------------------------------

            if name in REGISTRY:

                try:
                    result = REGISTRY[name](**args)

                except Exception as error:

                    result = (
                        f"Tool execution error: {error}"
                    )

            else:

                result = (
                    f"Error: no tool named '{name}'. "
                    f"Available tools: {list(REGISTRY)}"
                )

            tool_log.append(
                f"Step {step}: {name}({args}) -> {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    return (
        f"The agent stopped after {max_steps} steps.",
        tool_log,
    )


# ============================================================
# STREAMLIT USER INTERFACE
# ============================================================

st.title("✈️ Weekend Trip Planner")

st.markdown(
    """
### Plan your perfect short trip with AI

Choose a destination, tell the AI how many days you have,
and let the agent build an itinerary using its available tools.
"""
)


# ------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------

city = st.selectbox(
    "📍 Choose your destination",
    list(ACTIVITIES.keys()),
)

days = st.number_input(
    "🗓️ Number of days",
    min_value=0.5,
    max_value=7.0,
    value=2.0,
    step=0.5,
)

preferences = st.text_area(
    "💭 What kind of trip do you want?",
    placeholder=(
        "Example: I love nature, mountains, "
        "sunrise views and relaxing activities."
    ),
)


# ------------------------------------------------------------
# GENERATE BUTTON
# ------------------------------------------------------------

if st.button(
    "🚀 Plan My Trip",
    type="primary",
):

    if not preferences.strip():

        preferences = (
            "Create a balanced trip with "
            "interesting sightseeing and nature."
        )

    goal = (
        f"Plan a {days}-day weekend trip in {city}. "
        f"The traveler says: {preferences}"
    )

    with st.spinner(
        "🤖 AI agent is planning your trip..."
    ):

        try:

            answer, tool_log = run_agent(
                goal,
                total_days=days,
                max_steps=8,
            )

            st.session_state.last_answer = answer
            st.session_state.last_tool_log = tool_log

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )


# ============================================================
# DISPLAY RESULT
# ============================================================

if "last_answer" in st.session_state:

    st.divider()

    st.subheader("🗺️ Your AI Itinerary")

    answer = st.session_state.last_answer

    # Clean HTML line-break tags generated by the AI
    answer = answer.replace("<br>", "\n")
    answer = answer.replace("<br/>", "\n")
    answer = answer.replace("<br />", "\n")

    st.markdown(answer)

# ============================================================
# TOOL EXECUTION LOG
# ============================================================

if "last_tool_log" in st.session_state:

    with st.expander(
        "🔧 View AI Agent Tool Calls"
    ):

        for log in st.session_state.last_tool_log:

            st.code(
                log,
                language="text",
            )


# ============================================================
# CURRENT ITINERARY STATE
# ============================================================

if st.session_state.get("trip_state"):

    state = st.session_state.trip_state

    if state["itinerary"]:

        st.divider()

        st.subheader("📋 Agent State")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Activities",
                len(state["itinerary"]),
            )

        with col2:

            st.metric(
                "Days Remaining",
                f"{state['days_remaining']:.1f}",
            )

        st.write(
            "**Activities selected:**"
        )

        for activity in state["itinerary"]:

            st.write(
                f"✅ {activity}"
            )