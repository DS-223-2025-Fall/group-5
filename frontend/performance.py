import streamlit as st

# Sample data for metrics and feedback
before_after_data = [
    {'metric': 'Revenue', 'before': 485000, 'after': 603000},
    {'metric': 'Conversion', 'before': 12.3, 'after': 18.4},
    {'metric': 'Avg Basket', 'before': 128, 'after': 156},
    {'metric': 'Bundle ROI', 'before': 0, 'after': 245},  # This will trigger the zero division error
]

customer_feedback = [
    {'name': 'Sarah Johnson', 'rating': 5, 'comment': 'Love the bundle recommendations!'},
    {'name': 'Michael Chen', 'rating': 5, 'comment': 'Great product combinations.'},
    {'name': 'Emily Davis', 'rating': 4, 'comment': 'Good suggestions, would like more customization.'},
    {'name': 'James Wilson', 'rating': 5, 'comment': 'The bundles make sense and offer real value.'},
]

# Function to render star rating
def render_stars(rating):
    return "★" * rating + "☆" * (5 - rating)

# Simplified performance feedback screen
def performance_screen():
    st.title("Performance Feedback")
    st.write("Track the impact of product bundling on your business metrics")

    # Key Metrics (Before vs After)
    st.subheader("Key Metrics Comparison")
    for metric in before_after_data:
        st.write(f"**{metric['metric']}**")
        st.write(f"Before: {metric['before']}")
        st.write(f"After: {metric['after']}")
        
        # Calculate percentage change with division by zero check
        if metric['before'] != 0:
            percentage_change = ((metric['after'] - metric['before']) / metric['before']) * 100
            st.write(f"Change: {percentage_change:.2f}%")
        else:
            st.write("Change: N/A (Division by zero)")
        
        st.write("---")

    # Customer Feedback
    st.subheader("Customer Feedback")
    for feedback in customer_feedback:
        st.write(f"**{feedback['name']}**")
        st.write(f"Rating: {render_stars(feedback['rating'])} ({feedback['rating']}/5)")
        st.write(f"Comment: {feedback['comment']}")
        st.write("---")

# Call the simplified performance screen
performance_screen()
