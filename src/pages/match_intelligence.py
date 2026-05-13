import streamlit as st

from src.pages.head_to_head import (
    show_head_to_head,
)

from src.pages.match_insights import (
    show_match_insights,
)

from src.pages.powerplay import (
    show_powerplay_analysis,
)

from src.pages.live_match_center import (
    show_live_match_center,
)


def show_match_intelligence(
    matches,
    deliveries,
    model
):

    st.title(
        "📊 Match Intelligence"
    )

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "⚔️ Head-to-Head",
        "🔥 Match Insights",
        "🚀 Powerplay & Death Overs",
        "📡 Live Match Center",
    ])

    # =====================================
    # TAB 1
    # =====================================

    with tab1:

        show_head_to_head(
            matches
        )

    # =====================================
    # TAB 2
    # =====================================

    with tab2:

        show_match_insights(
            matches,
            deliveries
        )

    # =====================================
    # TAB 3
    # =====================================

    with tab3:

        show_powerplay_analysis(
            deliveries
        )

    # =====================================
    # TAB 4
    # =====================================

    with tab4:

        show_live_match_center(
            matches,
            model
        )