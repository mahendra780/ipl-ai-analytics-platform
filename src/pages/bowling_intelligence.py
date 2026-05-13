import streamlit as st

from src.pages.bowling import (
    show_bowling_analytics,
)

from src.pages.bowler_profile import (
    show_bowler_profile,
)

from src.pages.bowling_phase import (
    show_bowling_phase_analytics,
)


def show_bowling_intelligence(
    deliveries
):

    st.title(
        "🎯 Bowling Intelligence"
    )

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📊 Bowling Analytics",
        "👤 Bowler Profile",
        "🔥 Phase Analytics",
    ])

    # =====================================
    # TAB 1
    # =====================================

    with tab1:

        show_bowling_analytics(
            deliveries
        )

    # =====================================
    # TAB 2
    # =====================================

    with tab2:

        show_bowler_profile(
            deliveries
        )

    # =====================================
    # TAB 3
    # =====================================

    with tab3:

        show_bowling_phase_analytics(
            deliveries
        )