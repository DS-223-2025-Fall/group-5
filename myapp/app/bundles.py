import streamlit as st

def bundles_screen():
    st.title("Bundle Suggestions")
    
    # Example input (e.g., selecting products)
    st.write("Select items to create a bundle:")

    items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    selected_items = st.multiselect("Choose items", items)
    
    if selected_items:
        st.write("You selected:", ", ".join(selected_items))
        # Example suggestion: Simply show the selected items as a bundle suggestion
        st.write(f"Suggested Bundle: {', '.join(selected_items)}")
    else:
        st.write("Select some items to get suggestions!")
