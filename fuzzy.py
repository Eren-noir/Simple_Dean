import streamlit as st
import numpy as np
import pandas as pd

# -------------------------------------------------
# Fuzzy Logic Functions
# -------------------------------------------------

def fuzzify(value, low_range, med_range, high_range):
    """Convert crisp value to fuzzy membership values"""
    fuzzy = {'low': 0, 'medium': 0, 'high': 0}
    
    # Low membership
    if value <= low_range[1]:
        fuzzy['low'] = 1
    elif value < med_range[0]:
        fuzzy['low'] = (med_range[0] - value) / (med_range[0] - low_range[1])
    
    # Medium membership
    if med_range[0] <= value <= med_range[1]:
        fuzzy['medium'] = 1
    elif low_range[1] < value < med_range[0]:
        fuzzy['medium'] = (value - low_range[1]) / (med_range[0] - low_range[1])
    elif med_range[1] < value < high_range[0]:
        fuzzy['medium'] = (high_range[0] - value) / (high_range[0] - med_range[1])
    
    # High membership
    if value >= high_range[0]:
        fuzzy['high'] = 1
    elif med_range[1] < value < high_range[0]:
        fuzzy['high'] = (value - med_range[1]) / (high_range[0] - med_range[1])
    
    return fuzzy

def apply_rules(moisture, temp, humidity):
    """Apply fuzzy rules and calculate irrigation level"""
    rules = []
    rule_descriptions = []
    
    # Rule 1: Dry soil + Hot + Dry air = Very High irrigation
    rules.append(min(moisture['low'], temp['high'], humidity['low']) * 90)
    rule_descriptions.append("Dry soil + Hot + Dry air → Very High")
    
    # Rule 2: Dry soil + Hot + Medium humidity = High irrigation
    rules.append(min(moisture['low'], temp['high'], humidity['medium']) * 85)
    rule_descriptions.append("Dry soil + Hot + Medium humidity → High")
    
    # Rule 3: Dry soil + Warm + Dry air = High irrigation
    rules.append(min(moisture['low'], temp['medium'], humidity['low']) * 80)
    rule_descriptions.append("Dry soil + Warm + Dry air → High")
    
    # Rule 4: Medium moisture + Hot + Dry air = Medium-High irrigation
    rules.append(min(moisture['medium'], temp['high'], humidity['low']) * 70)
    rule_descriptions.append("Medium moisture + Hot + Dry air → Medium-High")
    
    # Rule 5: Dry soil + Warm + Medium humidity = Medium-High irrigation
    rules.append(min(moisture['low'], temp['medium'], humidity['medium']) * 75)
    rule_descriptions.append("Dry soil + Warm + Medium humidity → Medium-High")
    
    # Rule 6: Medium moisture + Hot + Medium humidity = Medium irrigation
    rules.append(min(moisture['medium'], temp['high'], humidity['medium']) * 60)
    rule_descriptions.append("Medium moisture + Hot + Medium humidity → Medium")
    
    # Rule 7: Medium moisture + Warm + Medium humidity = Medium irrigation
    rules.append(min(moisture['medium'], temp['medium'], humidity['medium']) * 50)
    rule_descriptions.append("Medium moisture + Warm + Medium humidity → Medium")
    
    # Rule 8: Dry soil + Cool + High humidity = Medium irrigation
    rules.append(min(moisture['low'], temp['low'], humidity['high']) * 45)
    rule_descriptions.append("Dry soil + Cool + High humidity → Medium")
    
    # Rule 9: Medium moisture + Cool + High humidity = Low irrigation
    rules.append(min(moisture['medium'], temp['low'], humidity['high']) * 30)
    rule_descriptions.append("Medium moisture + Cool + High humidity → Low")
    
    # Rule 10: Wet soil + High humidity = Very Low irrigation
    rules.append(min(moisture['high'], humidity['high']) * 15)
    rule_descriptions.append("Wet soil + High humidity → Very Low")
    
    # Rule 11: Wet soil + Cool = Very Low irrigation
    rules.append(min(moisture['high'], temp['low']) * 10)
    rule_descriptions.append("Wet soil + Cool → Very Low")
    
    # Rule 12: Wet soil + Medium conditions = Low irrigation
    rules.append(min(moisture['high'], temp['medium'], humidity['medium']) * 20)
    rule_descriptions.append("Wet soil + Medium conditions → Low")
    
    # Calculate defuzzified output using weighted average
    numerator = sum(rules)
    weights = [90, 85, 80, 70, 75, 60, 50, 45, 30, 15, 10, 20]
    denominator = sum([r/w if w != 0 else 0 for r, w in zip(rules, weights)])
    
    irrigation_level = numerator / denominator if denominator > 0 else 50
    
    # Get active rules (strength > 0.1)
    active_rules = [(desc, strength) for desc, strength in zip(rule_descriptions, rules) if strength > 0.1]
    
    return irrigation_level, active_rules

def plot_membership_functions(value, low_range, med_range, high_range, title):
    """Plot fuzzy membership functions using matplotlib"""
    x = np.linspace(0, 100, 200)
    low_membership = []
    med_membership = []
    high_membership = []
    
    for val in x:
        fuzzy = fuzzify(val, low_range, med_range, high_range)
        low_membership.append(fuzzy['low'])
        med_membership.append(fuzzy['medium'])
        high_membership.append(fuzzy['high'])
    
    # Create DataFrame for streamlit line chart
    df = pd.DataFrame({
        'x': x,
        'Low': low_membership,
        'Medium': med_membership,
        'High': high_membership
    })
    
    return df, value

def get_recommendation_details(level):
    """Get detailed recommendations based on irrigation level"""
    if level < 25:
        category = "MINIMAL"
        color = "🔵"
        advice = "Soil moisture is adequate. Monitor conditions but minimal watering needed."
        duration = "5-10 minutes"
    elif level < 45:
        category = "LOW"
        color = "🟢"
        advice = "Light irrigation recommended. Water early morning or evening."
        duration = "15-20 minutes"
    elif level < 65:
        category = "MEDIUM"
        color = "🟡"
        advice = "Moderate irrigation needed. Ensure even distribution across field."
        duration = "25-35 minutes"
    elif level < 80:
        category = "HIGH"
        color = "🟠"
        advice = "Significant irrigation required. Check soil penetration depth."
        duration = "40-50 minutes"
    else:
        category = "CRITICAL"
        color = "🔴"
        advice = "Immediate irrigation necessary! Crops at risk. Water deeply and thoroughly."
        duration = "60+ minutes"
    
    return category, color, advice, duration

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Fuzzy Irrigation System",
    page_icon="🌾",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------

st.markdown("""
    <h1 style='text-align: center; color: #2e7d32;'>
        🌾 Intelligent Fuzzy Logic Irrigation System
    </h1>
    <p style='text-align: center; font-size: 1.1em; color: #666;'>
        AI-Powered Water Management for Optimal Crop Growth
    </p>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# Sidebar Information
# -------------------------------------------------

with st.sidebar:
    st.header("ℹ️ System Information")
    st.markdown("""
    ### How It Works
    
    This system uses **fuzzy logic** to make intelligent irrigation decisions based on:
    
    - 🌱 **Soil Moisture**: Current water content
    - 🌡️ **Temperature**: Ambient temperature
    - 💨 **Humidity**: Air moisture level
    
    ### Fuzzy Logic Process
    
    1. **Fuzzification**: Convert sensor readings to fuzzy sets
    2. **Rule Application**: Apply 12 expert rules
    3. **Defuzzification**: Calculate precise irrigation level
    
    ### Benefits
    
    ✅ Water conservation  
    ✅ Optimal crop health  
    ✅ Reduced costs  
    ✅ Automated decision-making
    """)
    
    st.divider()
    
    st.markdown("""
    ### Membership Ranges
    
    **Soil Moisture:**
    - Low: 0-30%
    - Medium: 25-55%
    - High: 50-100%
    
    **Temperature:**
    - Low: 0-20°C
    - Medium: 15-30°C
    - High: 25-50°C
    
    **Humidity:**
    - Low: 0-35%
    - Medium: 30-60%
    - High: 55-100%
    """)

# -------------------------------------------------
# Main Interface
# -------------------------------------------------

st.header("📊 Environmental Sensors")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💧 Soil Moisture")
    moisture = st.slider("Soil Moisture (%)", 0, 100, 50, 
                        help="Current soil moisture percentage")
    if moisture < 30:
        st.warning("⚠️ Low moisture detected")
    elif moisture > 70:
        st.info("💧 High moisture level")

with col2:
    st.markdown("### 🌡️ Temperature")
    temp = st.slider("Temperature (°C)", 0, 50, 25,
                    help="Ambient temperature in Celsius")
    if temp > 35:
        st.warning("🔥 High temperature!")
    elif temp < 15:
        st.info("❄️ Cool conditions")

with col3:
    st.markdown("### 💨 Air Humidity")
    humidity = st.slider("Humidity (%)", 0, 100, 50,
                        help="Relative humidity percentage")
    if humidity < 30:
        st.warning("🏜️ Very dry air")
    elif humidity > 70:
        st.info("💦 High humidity")

st.divider()

# -------------------------------------------------
# Calculate Button
# -------------------------------------------------

if st.button("🚀 Calculate Irrigation Level", type="primary", use_container_width=True):
    
    # Fuzzify inputs
    moisture_fuzzy = fuzzify(moisture, [0, 30], [25, 55], [50, 100])
    temp_fuzzy = fuzzify(temp, [0, 20], [15, 30], [25, 50])
    humidity_fuzzy = fuzzify(humidity, [0, 35], [30, 60], [55, 100])
    
    # Apply rules
    irrigation_level, active_rules = apply_rules(moisture_fuzzy, temp_fuzzy, humidity_fuzzy)
    
    # Get recommendations
    category, color, advice, duration = get_recommendation_details(irrigation_level)
    
    # -------------------------------------------------
    # Results Display
    # -------------------------------------------------
    
    st.header("🎯 Irrigation Recommendation")
    
    # Main result card
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32;'>
            <h2 style='margin: 0; color: #2e7d32;'>{color} {category} IRRIGATION</h2>
            <p style='font-size: 1.1em; margin-top: 10px;'>{advice}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Irrigation Level", f"{irrigation_level:.1f}%", 
                 delta=f"{irrigation_level - 50:.1f}% from baseline")
    
    with col3:
        st.metric("Duration", duration)
    
    # Progress bar
    st.progress(irrigation_level / 100)
    
    st.divider()
    
    # -------------------------------------------------
    # Fuzzy Membership Visualization
    # -------------------------------------------------
    
    st.header("📈 Fuzzy Membership Functions")
    
    tab1, tab2, tab3 = st.tabs(["💧 Soil Moisture", "🌡️ Temperature", "💨 Humidity"])
    
    with tab1:
        st.markdown(f"**Soil Moisture Membership Functions** (Current: {moisture}%)")
        df1, current_val = plot_membership_functions(moisture, [0, 30], [25, 55], [50, 100], 
                                        "Soil Moisture Membership Functions")
        st.line_chart(df1.set_index('x'), color=['#0000FF', '#00FF00', '#FF0000'])
        st.caption(f"Current value: {moisture}%")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Low", f"{moisture_fuzzy['low']:.3f}")
        col2.metric("Medium", f"{moisture_fuzzy['medium']:.3f}")
        col3.metric("High", f"{moisture_fuzzy['high']:.3f}")
    
    with tab2:
        st.markdown(f"**Temperature Membership Functions** (Current: {temp}°C)")
        df2, current_val = plot_membership_functions(temp, [0, 20], [15, 30], [25, 50],
                                        "Temperature Membership Functions")
        st.line_chart(df2.set_index('x'), color=['#0000FF', '#00FF00', '#FF0000'])
        st.caption(f"Current value: {temp}°C")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Low", f"{temp_fuzzy['low']:.3f}")
        col2.metric("Medium", f"{temp_fuzzy['medium']:.3f}")
        col3.metric("High", f"{temp_fuzzy['high']:.3f}")
    
    with tab3:
        st.markdown(f"**Humidity Membership Functions** (Current: {humidity}%)")
        df3, current_val = plot_membership_functions(humidity, [0, 35], [30, 60], [55, 100],
                                        "Humidity Membership Functions")
        st.line_chart(df3.set_index('x'), color=['#0000FF', '#00FF00', '#FF0000'])
        st.caption(f"Current value: {humidity}%")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Low", f"{humidity_fuzzy['low']:.3f}")
        col2.metric("Medium", f"{humidity_fuzzy['medium']:.3f}")
        col3.metric("High", f"{humidity_fuzzy['high']:.3f}")
    
    st.divider()
    
    # -------------------------------------------------
    # Active Rules
    # -------------------------------------------------
    
    st.header("⚡ Active Fuzzy Rules")
    
    if active_rules:
        st.markdown(f"**{len(active_rules)} rules were triggered** (strength > 0.1)")
        
        # Sort by strength
        active_rules.sort(key=lambda x: x[1], reverse=True)
        
        for i, (description, strength) in enumerate(active_rules, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{i}.** {description}")
            with col2:
                st.metric("Strength", f"{strength:.2f}")
            st.progress(strength / max([r[1] for r in active_rules]))
            st.markdown("---")
    else:
        st.info("No rules were strongly activated with current conditions.")
    
    st.divider()
    
    # -------------------------------------------------
    # Additional Insights
    # -------------------------------------------------
    
    st.header("💡 Additional Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Condition Analysis")
        
        # Moisture analysis
        if moisture < 30:
            st.warning("🌵 **Dry Soil**: Immediate attention needed")
        elif moisture > 70:
            st.success("💧 **Moist Soil**: Good water retention")
        else:
            st.info("✅ **Adequate Moisture**: Normal range")
        
        # Temperature analysis
        if temp > 35:
            st.warning("🔥 **High Heat**: Increased evaporation expected")
        elif temp < 15:
            st.info("❄️ **Cool Weather**: Lower water demand")
        else:
            st.success("🌡️ **Optimal Temperature**: Ideal growing conditions")
        
        # Humidity analysis
        if humidity < 30:
            st.warning("🏜️ **Low Humidity**: Faster soil moisture loss")
        elif humidity > 70:
            st.info("💦 **High Humidity**: Slower evaporation rate")
        else:
            st.success("💨 **Balanced Humidity**: Normal conditions")
    
    with col2:
        st.subheader("Best Practices")
        st.markdown("""
        **Watering Tips:**
        - 🌅 Water during early morning (6-9 AM)
        - 🌙 Or late evening (6-8 PM)
        - 💧 Avoid midday watering
        - 🌊 Check for even water distribution
        - 📏 Monitor soil penetration depth
        
        **Monitoring:**
        - 📊 Track daily moisture levels
        - 📈 Record irrigation amounts
        - 🌱 Observe crop response
        - 🔄 Adjust based on weather forecasts
        """)

else:
    st.info("👆 Adjust the environmental sensors above and click **Calculate Irrigation Level** to get recommendations")

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌾 <strong>Fuzzy Logic Irrigation System</strong> | Powered by AI & Expert Knowledge</p>
    <p style='font-size: 0.9em;'>Saving water, optimizing growth, maximizing yields</p>
</div>
""", unsafe_allow_html=True)