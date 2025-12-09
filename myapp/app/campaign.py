import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def campaigns_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">📢 Campaign Management</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Create and manage marketing campaigns for your product bundles'
        '</p>',
        unsafe_allow_html=True,
    )
    
    # Initialize campaigns in session
    if 'campaigns' not in st.session_state:
        st.session_state.campaigns = []
    
    # Check if creating campaign from bundle
    if st.session_state.get('campaign_bundle'):
        create_campaign_form()
    else:
        show_campaigns_list()


def create_campaign_form():
    """Form to create a new campaign from a bundle."""
    bundle = st.session_state.campaign_bundle
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Create New Campaign")
    
    st.markdown(f"**Selected Bundle:** `{bundle['products']}`")
    st.markdown(f"**Success Probability:** {bundle['success_probability']*100:.1f}%")
    
    st.markdown("---")
    
    with st.form("campaign_form"):
        # Campaign details
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input(
                "Campaign Name *",
                value=f"{bundle['products']} Bundle Offer",
                help="Give your campaign a memorable name"
            )
            
            campaign_type = st.selectbox(
                "Campaign Type *",
                ["Email", "Social Media", "Website Banner", "Push Notification", "In-Store Display"],
                help="Where will this campaign run?"
            )
            
            discount_type = st.selectbox(
                "Discount Type",
                ["Percentage Off", "Fixed Amount", "Buy One Get One", "Free Shipping", "No Discount"],
            )
        
        with col2:
            start_date = st.date_input(
                "Start Date *",
                value=datetime.now(),
                help="When should the campaign begin?"
            )
            
            end_date = st.date_input(
                "End Date *",
                value=datetime.now() + timedelta(days=30),
                help="When should the campaign end?"
            )
            
            if discount_type == "Percentage Off":
                discount_value = st.slider("Discount Percentage", 5, 50, 15, step=5)
            elif discount_type == "Fixed Amount":
                discount_value = st.number_input("Discount Amount ($)", 5.0, 100.0, 10.0, step=5.0)
            else:
                discount_value = 0
        
        # Target audience
        st.markdown("**🎯 Target Audience**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_segment = st.multiselect(
                "Customer Segment",
                ["All Customers", "High Value", "Medium Value", "New Customers", "At Risk"],
                default=["All Customers"]
            )
        
        with col2:
            min_order_value = st.number_input("Minimum Order Value ($)", 0, 500, 0, step=10)
        
        with col3:
            budget = st.number_input("Campaign Budget ($)", 100, 50000, 1000, step=100)
        
        # Description
        description = st.text_area(
            "Campaign Description",
            value=f"Special bundle offer: {bundle['products']}. Buy together and save!",
            help="Describe your campaign message"
        )
        
        # Submit buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("🚀 Create Campaign", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
    
    if submit:
        if not campaign_name:
            st.error("Please provide a campaign name")
        elif end_date <= start_date:
            st.error("End date must be after start date")
        else:
            # Create campaign
            campaign = {
                'id': len(st.session_state.campaigns) + 1,
                'name': campaign_name,
                'bundle': bundle['products'],
                'bundle_data': bundle,
                'type': campaign_type,
                'discount_type': discount_type,
                'discount_value': discount_value,
                'start_date': start_date,
                'end_date': end_date,
                'target_segment': target_segment,
                'min_order_value': min_order_value,
                'budget': budget,
                'description': description,
                'status': 'Draft',
                'created_at': datetime.now(),
                'impressions': 0,
                'clicks': 0,
                'conversions': 0,
                'revenue': 0
            }
            
            st.session_state.campaigns.append(campaign)
            st.session_state.campaign_bundle = None
            st.success(f"✅ Campaign '{campaign_name}' created successfully!")
            st.rerun()
    
    if cancel:
        st.session_state.campaign_bundle = None
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def show_campaigns_list():
    """Display list of all campaigns."""
    campaigns = st.session_state.campaigns
    
    if not campaigns:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("📭 No campaigns yet. Create your first campaign from the Bundle Suggestions page!")
        st.markdown("**How to create a campaign:**")
        st.markdown("1. Go to **Bundle Suggestions**")
        st.markdown("2. Click **Generate Bundle Recommendations**")
        st.markdown("3. Click **Create Campaign** on any bundle")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Summary metrics
    st.markdown("")
    col1, col2, col3, col4 = st.columns(4)
    
    active_campaigns = sum(1 for c in campaigns if c['status'] == 'Active')
    total_budget = sum(c['budget'] for c in campaigns)
    total_conversions = sum(c['conversions'] for c in campaigns)
    total_revenue = sum(c['revenue'] for c in campaigns)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("📊 Total Campaigns", len(campaigns))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("✅ Active", active_campaigns)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("💰 Total Budget", f"${total_budget:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("💵 Revenue", f"${total_revenue:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Campaigns list
    st.markdown("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 All Campaigns")
    
    # Filter
    filter_status = st.selectbox(
        "Filter by status",
        ["All", "Draft", "Active", "Paused", "Completed"],
        key="status_filter"
    )
    
    filtered_campaigns = campaigns if filter_status == "All" else [c for c in campaigns if c['status'] == filter_status]
    
    if not filtered_campaigns:
        st.info(f"No {filter_status.lower()} campaigns found.")
    else:
        for campaign in filtered_campaigns:
            with st.expander(f"**{campaign['name']}** - {campaign['status']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Bundle:** {campaign['bundle']}")
                    st.markdown(f"**Type:** {campaign['type']}")
                    st.markdown(f"**Period:** {campaign['start_date']} to {campaign['end_date']}")
                    st.markdown(f"**Description:** {campaign['description']}")
                    
                    if campaign['discount_type'] != "No Discount":
                        if campaign['discount_type'] == "Percentage Off":
                            st.markdown(f"**Offer:** {campaign['discount_value']}% off")
                        elif campaign['discount_type'] == "Fixed Amount":
                            st.markdown(f"**Offer:** ${campaign['discount_value']} off")
                        else:
                            st.markdown(f"**Offer:** {campaign['discount_type']}")
                
                with col2:
                    st.markdown("**📊 Performance:**")
                    st.markdown(f"- Impressions: {campaign['impressions']:,}")
                    st.markdown(f"- Clicks: {campaign['clicks']:,}")
                    st.markdown(f"- Conversions: {campaign['conversions']:,}")
                    st.markdown(f"- Revenue: ${campaign['revenue']:,.2f}")
                    
                    if campaign['clicks'] > 0:
                        ctr = (campaign['clicks'] / campaign['impressions'] * 100) if campaign['impressions'] > 0 else 0
                        cvr = (campaign['conversions'] / campaign['clicks'] * 100) if campaign['clicks'] > 0 else 0
                        st.markdown(f"- CTR: {ctr:.1f}%")
                        st.markdown(f"- CVR: {cvr:.1f}%")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if campaign['status'] == 'Draft':
                        if st.button("▶️ Launch", key=f"launch_{campaign['id']}", use_container_width=True):
                            campaign['status'] = 'Active'
                            st.success("Campaign launched!")
                            st.rerun()
                
                with col2:
                    if campaign['status'] == 'Active':
                        if st.button("⏸️ Pause", key=f"pause_{campaign['id']}", use_container_width=True):
                            campaign['status'] = 'Paused'
                            st.success("Campaign paused")
                            st.rerun()
                    elif campaign['status'] == 'Paused':
                        if st.button("▶️ Resume", key=f"resume_{campaign['id']}", use_container_width=True):
                            campaign['status'] = 'Active'
                            st.success("Campaign resumed")
                            st.rerun()
                
                with col3:
                    if st.button("📊 View Analytics", key=f"analytics_{campaign['id']}", use_container_width=True):
                        st.info("Analytics dashboard coming soon!")
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{campaign['id']}", use_container_width=True):
                        st.session_state.campaigns = [c for c in campaigns if c['id'] != campaign['id']]
                        st.success("Campaign deleted")
                        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)