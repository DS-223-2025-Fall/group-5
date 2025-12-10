import streamlit as st
import pandas as pd
import altair as alt


def dashboard_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">Sales & Product Analytics Overview</p>',
        unsafe_allow_html=True,
    )

    all_data = st.session_state.get("all_tables_data", {})
    
    if not all_data:
        st.warning("Please load data from the **Database** page first.")
        return

    # Try to get the key tables
    sales_df = all_data.get("sales")
    products_df = all_data.get("products")
    transactions_df = all_data.get("transactions")
    customers_df = all_data.get("customers")
    timeframe_df = all_data.get("timeframe")

    # === KEY METRICS ===
    st.markdown("### 📊 Key Metrics")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if sales_df is not None:
            total_revenue = sales_df["line_total"].sum()
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        else:
            st.metric("Total Revenue", "N/A")
    
    with c2:
        if transactions_df is not None:
            total_transactions = len(transactions_df)
            st.metric("Transactions", f"{total_transactions:,}")
        else:
            st.metric("Transactions", "N/A")
    
    with c3:
        if products_df is not None:
            total_products = len(products_df)
            st.metric("Products", f"{total_products:,}")
        else:
            st.metric("Products", "N/A")
    
    with c4:
        if customers_df is not None:
            total_customers = len(customers_df)
            st.metric("Customers", f"{total_customers:,}")
        else:
            st.metric("Customers", "N/A")

    st.markdown("---")

    # === CUSTOMER SEGMENTATION (NEW) ===
    if customers_df is not None and not customers_df.empty:
        st.markdown("### 👥 Customer Segmentation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'gender' in customers_df.columns:
                st.markdown("#### Gender Distribution")
                gender_counts = customers_df['gender'].value_counts().reset_index()
                gender_counts.columns = ['Gender', 'Count']
                
                chart = alt.Chart(gender_counts).mark_arc(innerRadius=30).encode(
                    theta='Count:Q',
                    color=alt.Color('Gender:N', scale=alt.Scale(scheme='set2')),
                    tooltip=['Gender', 'Count']
                ).properties(height=200)
                st.altair_chart(chart, use_container_width=True)
        
        with col2:
            if 'age' in customers_df.columns:
                st.markdown("#### Age Distribution")
                age_data = customers_df['age'].dropna()
                
                chart = alt.Chart(pd.DataFrame({'age': age_data})).mark_bar(color='#3b82f6').encode(
                    x=alt.X('age:Q', bin=alt.Bin(maxbins=10), title='Age'),
                    y=alt.Y('count()', title='Count'),
                    tooltip=['count()']
                ).properties(height=200)
                st.altair_chart(chart, use_container_width=True)
        
        with col3:
            if 'income_level' in customers_df.columns:
                st.markdown("#### Income Levels")
                income_counts = customers_df['income_level'].value_counts().reset_index()
                income_counts.columns = ['Income', 'Count']
                
                # Define order
                order = ['Low', 'Medium', 'High', 'Premium']
                income_counts['Income'] = pd.Categorical(income_counts['Income'], categories=order, ordered=True)
                income_counts = income_counts.sort_values('Income')
                
                chart = alt.Chart(income_counts).mark_bar(color='#10b981').encode(
                    x=alt.X('Income:N', sort=order),
                    y='Count:Q',
                    tooltip=['Income', 'Count']
                ).properties(height=200)
                st.altair_chart(chart, use_container_width=True)
        
        with col4:
            if 'customer_segment' in customers_df.columns:
                st.markdown("#### Customer Segments")
                segment_counts = customers_df['customer_segment'].value_counts().reset_index()
                segment_counts.columns = ['Segment', 'Count']
                
                chart = alt.Chart(segment_counts).mark_arc(innerRadius=30).encode(
                    theta='Count:Q',
                    color=alt.Color('Segment:N', scale=alt.Scale(scheme='category20')),
                    tooltip=['Segment', 'Count']
                ).properties(height=200)
                st.altair_chart(chart, use_container_width=True)
        
        st.markdown("---")

    # === SALES CHARTS ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Monthly Sales")
        if sales_df is not None and transactions_df is not None and timeframe_df is not None:
            # Join sales -> transactions -> timeframe
            merged = sales_df.merge(transactions_df[["transaction_id", "time_id"]], on="transaction_id")
            merged = merged.merge(timeframe_df[["time_id", "month", "year"]], on="time_id")
            
            monthly_sales = merged.groupby("month")["line_total"].sum().reset_index()
            monthly_sales.columns = ["Month", "Sales"]
            
            month_names = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
                          7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
            monthly_sales["Month Name"] = monthly_sales["Month"].map(month_names)
            
            chart = alt.Chart(monthly_sales).mark_bar(color="#3b82f6", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X("Month Name:N", sort=list(month_names.values()), title="Month"),
                y=alt.Y("Sales:Q", title="Sales ($)"),
                tooltip=["Month Name", alt.Tooltip("Sales:Q", format="$,.0f")]
            ).properties(height=280)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Sales/timeframe data not available")
    
    with col2:
        st.markdown("#### Product Categories Distribution")
        if products_df is not None and "category" in products_df.columns:
            category_counts = products_df["category"].value_counts().reset_index()
            category_counts.columns = ["Category", "Count"]
            
            pie_chart = alt.Chart(category_counts).mark_arc(innerRadius=50).encode(
                theta=alt.Theta("Count:Q"),
                color=alt.Color("Category:N", scale=alt.Scale(scheme="category10")),
                tooltip=["Category", "Count"]
            ).properties(height=280)
            st.altair_chart(pie_chart, use_container_width=True)
        else:
            st.info("Product category data not available")

    st.markdown("---")

    # === SALES BY CUSTOMER SEGMENT (NEW) ===
    if sales_df is not None and transactions_df is not None and customers_df is not None:
        if 'customer_segment' in customers_df.columns:
            st.markdown("#### Sales by Customer Segment")
            
            # Merge to get customer segments
            merged = sales_df.merge(transactions_df[['transaction_id', 'customer_id']], on='transaction_id')
            merged = merged.merge(customers_df[['customer_id', 'customer_segment']], on='customer_id')
            
            segment_sales = merged.groupby('customer_segment')['line_total'].sum().reset_index()
            segment_sales.columns = ['Segment', 'Revenue']
            segment_sales = segment_sales.sort_values('Revenue', ascending=False)
            
            chart = alt.Chart(segment_sales).mark_bar(color='#8b5cf6').encode(
                x=alt.X('Segment:N', sort='-y', title='Customer Segment'),
                y=alt.Y('Revenue:Q', title='Revenue ($)'),
                tooltip=['Segment', alt.Tooltip('Revenue:Q', format='$,.0f')]
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)
            
            st.markdown("---")

    # === MORE ANALYTICS ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Products by Revenue")
        if sales_df is not None and products_df is not None:
            product_revenue = sales_df.groupby("product_sku")["line_total"].sum().reset_index()
            product_revenue = product_revenue.merge(products_df[["product_sku", "product_name"]], on="product_sku")
            product_revenue = product_revenue.nlargest(10, "line_total")
            
            chart = alt.Chart(product_revenue).mark_bar(color="#10b981").encode(
                x=alt.X("line_total:Q", title="Revenue ($)"),
                y=alt.Y("product_name:N", sort="-x", title="Product"),
                tooltip=["product_name", alt.Tooltip("line_total:Q", format="$,.0f")]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Product sales data not available")
    
    with col2:
        st.markdown("#### Sales by Channel")
        if transactions_df is not None and "channel" in transactions_df.columns:
            channel_data = transactions_df["channel"].value_counts().reset_index()
            channel_data.columns = ["Channel", "Count"]
            
            chart = alt.Chart(channel_data).mark_arc(innerRadius=50).encode(
                theta="Count:Q",
                color=alt.Color("Channel:N", scale=alt.Scale(scheme="set2")),
                tooltip=["Channel", "Count"]
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Channel data not available")

    st.markdown("---")

    # === TOP BRANDS ===
    st.markdown("#### Top Brands by Revenue")
    if sales_df is not None and products_df is not None and "brand" in products_df.columns:
        brand_revenue = sales_df.merge(products_df[["product_sku", "brand"]], on="product_sku")
        brand_totals = brand_revenue.groupby("brand")["line_total"].sum().reset_index()
        brand_totals = brand_totals.nlargest(10, "line_total")
        
        chart = alt.Chart(brand_totals).mark_bar(color="#8b5cf6").encode(
            x=alt.X("brand:N", sort="-y", title="Brand"),
            y=alt.Y("line_total:Q", title="Revenue ($)"),
            tooltip=["brand", alt.Tooltip("line_total:Q", format="$,.0f")]
        ).properties(height=250)
        st.altair_chart(chart, use_container_width=True)

    # === PAYMENT METHODS ===
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Payment Methods")
        if transactions_df is not None and "payment_type" in transactions_df.columns:
            payment_data = transactions_df["payment_type"].value_counts().reset_index()
            payment_data.columns = ["Payment", "Count"]
            st.dataframe(payment_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Average Transaction Value")
        if transactions_df is not None:
            avg_value = transactions_df["transaction_amount"].mean()
            max_value = transactions_df["transaction_amount"].max()
            min_value = transactions_df["transaction_amount"].min()
            
            st.metric("Average", f"${avg_value:,.2f}")
            st.metric("Max", f"${max_value:,.2f}")
            st.metric("Min", f"${min_value:,.2f}")