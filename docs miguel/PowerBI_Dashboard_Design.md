# Health & Fitness Analytics Platform - Power BI Dashboard Design

**Author:** Miguel Nemenzo
**Date:** December 2025  
**Version:** 1.0

---

## Executive Summary

This document outlines the design and implementation strategy for the **Health & Fitness Analytics Platform Power BI Dashboard**. The dashboard provides actionable insights for fitness facility management, enabling data-driven decisions to improve member engagement, optimize operations, and drive revenue growth.

---

## Business Objectives

### Primary Goals

1. **Increase Member Retention**: Identify at-risk members and implement targeted retention strategies
2. **Optimize Facility Operations**: Understand peak usage times and resource allocation needs
3. **Enhance Member Experience**: Track engagement patterns and personalize fitness programs
4. **Drive Revenue Growth**: Identify upsell opportunities and membership upgrade potential
5. **Improve Health Outcomes**: Monitor member progress toward fitness goals

### Key Performance Indicators (KPIs)

- **Member Retention Rate**: Percentage of active members month-over-month
- **Average Engagement Score**: Member interaction and activity levels
- **Workout Frequency**: Average workouts per member per week
- **Nutrition Adherence**: Percentage of members logging meals regularly
- **At-Risk Members**: Count of members with declining engagement
- **Revenue Per Member**: Average monthly revenue per active member

---

## Dashboard Architecture

### Dashboard Structure

The Power BI solution consists of **4 interconnected dashboards**:

1. **Executive Overview Dashboard** - High-level KPIs and trends
2. **Member Analytics Dashboard** - Individual member insights and segmentation
3. **Workout & Nutrition Dashboard** - Activity patterns and health metrics
4. **Operational Insights Dashboard** - Facility utilization and resource planning

---

## 1. Executive Overview Dashboard

### Purpose
Provide C-level executives and facility managers with a comprehensive view of business health and performance trends.

### Key Visualizations

#### 1.1 KPI Cards (Top Row)
- **Total Active Members** (with MoM % change)
- **Member Retention Rate** (with trend indicator)
- **Average Engagement Score** (0-100 scale)
- **Total Workouts This Month** (with YoY comparison)
- **Revenue This Month** (with target vs. actual)
- **At-Risk Members** (with alert threshold)

#### 1.2 Member Growth Trend (Line Chart)
- **X-Axis**: Month
- **Y-Axis**: Member count
- **Series**: 
  - Total Members
  - Active Members
  - New Members
  - Churned Members
- **Filters**: Date range, membership type

#### 1.3 Engagement Distribution (Donut Chart)
- **Segments**: 
  - High Engagement (70-100)
  - Medium Engagement (40-69)
  - Low Engagement (0-39)
- **Metric**: Member count and percentage

#### 1.4 Revenue by Membership Type (Stacked Bar Chart)
- **X-Axis**: Membership type (Premium, Standard, Basic)
- **Y-Axis**: Revenue
- **Color**: Monthly comparison

#### 1.5 Daily Activity Heatmap (Matrix Visual)
- **Rows**: Day of week
- **Columns**: Hour of day
- **Values**: Check-in count
- **Color Scale**: Low (blue) to High (red)

#### 1.6 Top Performing Metrics (Table)
- Most popular exercises
- Most active members
- Peak usage times
- Highest engagement segments

### Filters & Slicers
- Date Range (Last 7 days, 30 days, 90 days, YTD, Custom)
- Membership Type
- Age Group
- Gender
- Facility Location (if multi-location)

### Data Sources
- `AGG_DAILY_KPI`
- `DIM_MEMBER`
- `FACT_MEMBER_ENGAGEMENT`
- `AGG_MEMBER_MONTHLY_SUMMARY`

---

## 2. Member Analytics Dashboard

### Purpose
Deep dive into member behavior, segmentation, and individual performance tracking.

### Key Visualizations

#### 2.1 Member Segmentation Matrix (Scatter Plot)
- **X-Axis**: Workout Frequency (workouts per month)
- **Y-Axis**: Engagement Score
- **Bubble Size**: Tenure (months)
- **Color**: Membership Type
- **Tooltip**: Member name, fitness goal, last activity date

#### 2.2 Member Demographics (Clustered Column Chart)
- **X-Axis**: Age Group
- **Y-Axis**: Member count
- **Series**: Gender
- **Drill-through**: Individual member details

#### 2.3 Fitness Goals Distribution (Pie Chart)
- **Segments**: Weight Loss, Muscle Gain, General Fitness, Athletic Performance, etc.
- **Metric**: Percentage of members

#### 2.4 Member Tenure Analysis (Histogram)
- **X-Axis**: Tenure category (New, Regular, Veteran)
- **Y-Axis**: Member count
- **Color**: Membership status (Active/Inactive)

#### 2.5 At-Risk Members Table (Detailed Table)
- **Columns**:
  - Member Name
  - Last Activity Date
  - Engagement Score
  - Days Since Last Workout
  - Recommended Action
- **Conditional Formatting**: Red for critical, yellow for warning

#### 2.6 Member Journey Timeline (Gantt-style Visual)
- Track individual member milestones
- Workout frequency over time
- Engagement score trends

### Filters & Slicers
- Member Name (Search)
- Membership Type
- Engagement Level
- Tenure Category
- Fitness Goal
- At-Risk Status

### Data Sources
- `DIM_MEMBER`
- `FACT_MEMBER_ENGAGEMENT`
- `AGG_MEMBER_MONTHLY_SUMMARY`

---

## 3. Workout & Nutrition Dashboard

### Purpose
Analyze workout patterns, exercise preferences, and nutrition habits to optimize programming and member outcomes.

### Key Visualizations

#### 3.1 Workout Volume Trends (Area Chart)
- **X-Axis**: Date
- **Y-Axis**: Total workout minutes
- **Series**: 
  - Total Volume (kg)
  - Calories Burned
  - Workout Count
- **Filters**: Exercise type, muscle group

#### 3.2 Exercise Popularity (Bar Chart)
- **X-Axis**: Exercise name
- **Y-Axis**: Number of times performed
- **Color**: Muscle group
- **Top N**: Top 20 exercises

#### 3.3 Muscle Group Distribution (Treemap)
- **Hierarchy**: 
  - Muscle Group Category (Upper/Lower/Core)
  - Specific Muscle Group
  - Exercise Type
- **Size**: Workout count

#### 3.4 Workout Intensity Analysis (Box Plot)
- **X-Axis**: Difficulty level (Beginner, Intermediate, Expert)
- **Y-Axis**: Intensity score
- **Outliers**: Highlight exceptional performances

#### 3.5 Nutrition Macro Balance (Stacked Area Chart)
- **X-Axis**: Date
- **Y-Axis**: Percentage
- **Series**: 
  - Protein %
  - Carbs %
  - Fat %
- **Target Line**: Ideal macro split (e.g., 40/30/30)

#### 3.6 Calorie Intake vs. Expenditure (Dual-Axis Line Chart)
- **X-Axis**: Date
- **Y-Axis (Primary)**: Calories consumed
- **Y-Axis (Secondary)**: Calories burned
- **Gap Analysis**: Surplus/deficit highlighting

#### 3.7 Meal Type Distribution (Donut Chart)
- **Segments**: Breakfast, Lunch, Dinner, Snacks
- **Metric**: Average calories per meal type

#### 3.8 Top Nutrition Sources (Table)
- Most logged foods
- Average macros per serving
- Food category distribution

### Filters & Slicers
- Date Range
- Member (Multi-select)
- Exercise Type
- Muscle Group
- Difficulty Level
- Meal Type

### Data Sources
- `FACT_WORKOUT_ACTIVITY`
- `DIM_EXERCISE`
- `FACT_NUTRITION_INTAKE`
- `DIM_NUTRITION`

---

## 4. Operational Insights Dashboard

### Purpose
Optimize facility operations, staffing, and resource allocation based on usage patterns.

### Key Visualizations

#### 4.1 Peak Hours Heatmap (Matrix)
- **Rows**: Day of week
- **Columns**: Hour of day (6 AM - 10 PM)
- **Values**: Check-in count
- **Conditional Formatting**: Traffic light colors

#### 4.2 Equipment Utilization (Gauge Charts)
- **Metrics**: 
  - Free Weights usage %
  - Cardio machines usage %
  - Strength machines usage %
- **Threshold**: Optimal utilization range

#### 4.3 Class Attendance Trends (Line Chart)
- **X-Axis**: Week
- **Y-Axis**: Attendance count
- **Series**: Class type (Yoga, Spin, HIIT, etc.)

#### 4.4 Trainer Session Demand (Clustered Bar Chart)
- **X-Axis**: Trainer name
- **Y-Axis**: Sessions booked
- **Color**: Time slot (Morning, Afternoon, Evening)

#### 4.5 Member Check-in Patterns (Waterfall Chart)
- **X-Axis**: Day of week
- **Y-Axis**: Check-in count
- **Comparison**: Week-over-week change

#### 4.6 Facility Capacity Planning (Combo Chart)
- **X-Axis**: Hour of day
- **Y-Axis (Primary)**: Current capacity usage (%)
- **Y-Axis (Secondary)**: Optimal capacity line
- **Alert**: Overcapacity warnings

### Filters & Slicers
- Date Range
- Day of Week
- Time of Day
- Facility Area

### Data Sources
- `FACT_MEMBER_ENGAGEMENT`
- `FACT_WORKOUT_ACTIVITY`
- `DIM_TIME`
- `DIM_DATE`

---

## Data Connection Setup

### Snowflake Connection Configuration

#### Connection Method: DirectQuery (Recommended)

**Advantages:**
- Real-time data access
- No data refresh scheduling needed
- Always up-to-date insights
- Reduced Power BI file size

**Configuration Steps:**

1. **Get Data** → **Snowflake**
2. **Server**: `<your_account>.snowflakecomputing.com`
3. **Warehouse**: `COMPUTE_WH`
4. **Database**: `ANALYTICS_FITNESS_DB`
5. **Authentication**: Username/Password or SSO

#### Alternative: Import Mode

For faster performance with smaller datasets or when offline access is needed.

**Configuration Steps:**
1. Same connection as DirectQuery
2. Select **Import** mode
3. Configure scheduled refresh (daily recommended)

### Tables to Import

#### Dimension Tables
- `ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE`
- `ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_TIME`
- `ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER`
- `ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_EXERCISE`
- `ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_NUTRITION`

#### Fact Tables
- `ANALYTICS_FITNESS_DB.FACTS.FACT_WORKOUT_ACTIVITY`
- `ANALYTICS_FITNESS_DB.FACTS.FACT_NUTRITION_INTAKE`
- `ANALYTICS_FITNESS_DB.FACTS.FACT_MEMBER_ENGAGEMENT`

#### Aggregate Tables
- `ANALYTICS_FITNESS_DB.AGGREGATES.AGG_MEMBER_MONTHLY_SUMMARY`
- `ANALYTICS_FITNESS_DB.AGGREGATES.AGG_DAILY_KPI`

---

## Data Model Relationships

### Star Schema Relationships

```
DIM_MEMBER (1) ----< (*) FACT_WORKOUT_ACTIVITY
DIM_MEMBER (1) ----< (*) FACT_NUTRITION_INTAKE
DIM_MEMBER (1) ----< (*) FACT_MEMBER_ENGAGEMENT

DIM_EXERCISE (1) ----< (*) FACT_WORKOUT_ACTIVITY
DIM_NUTRITION (1) ----< (*) FACT_NUTRITION_INTAKE

DIM_DATE (1) ----< (*) FACT_WORKOUT_ACTIVITY
DIM_DATE (1) ----< (*) FACT_NUTRITION_INTAKE
DIM_DATE (1) ----< (*) FACT_MEMBER_ENGAGEMENT

DIM_TIME (1) ----< (*) FACT_WORKOUT_ACTIVITY
```

### Relationship Configuration

- **Cardinality**: One-to-Many (1:*)
- **Cross-filter Direction**: Single (from dimension to fact)
- **Make this relationship active**: Yes
- **Assume referential integrity**: Yes (for DirectQuery performance)

---

## DAX Measures

### Key Calculated Measures

#### Member Metrics

```dax
Total Members = DISTINCTCOUNT(DIM_MEMBER[member_id])

Active Members = 
CALCULATE(
    DISTINCTCOUNT(DIM_MEMBER[member_id]),
    DIM_MEMBER[membership_status] = "Active"
)

Member Retention Rate = 
DIVIDE(
    [Active Members],
    [Total Members],
    0
) * 100

New Members This Month = 
CALCULATE(
    DISTINCTCOUNT(DIM_MEMBER[member_id]),
    DIM_MEMBER[join_date] >= DATE(YEAR(TODAY()), MONTH(TODAY()), 1)
)

At-Risk Members = 
CALCULATE(
    DISTINCTCOUNT(FACT_MEMBER_ENGAGEMENT[member_key]),
    FACT_MEMBER_ENGAGEMENT[is_at_risk] = TRUE
)
```

#### Workout Metrics

```dax
Total Workouts = COUNTROWS(FACT_WORKOUT_ACTIVITY)

Avg Workouts Per Member = 
DIVIDE(
    [Total Workouts],
    [Active Members],
    0
)

Total Calories Burned = SUM(FACT_WORKOUT_ACTIVITY[calories_burned])

Avg Workout Duration = AVERAGE(FACT_WORKOUT_ACTIVITY[duration_minutes])

Total Volume Lifted = SUM(FACT_WORKOUT_ACTIVITY[total_volume_kg])
```

#### Engagement Metrics

```dax
Avg Engagement Score = AVERAGE(FACT_MEMBER_ENGAGEMENT[engagement_score])

High Engagement Members = 
CALCULATE(
    DISTINCTCOUNT(FACT_MEMBER_ENGAGEMENT[member_key]),
    FACT_MEMBER_ENGAGEMENT[engagement_level] = "High"
)

Total Check-Ins = SUM(FACT_MEMBER_ENGAGEMENT[check_ins])
```

#### Nutrition Metrics

```dax
Avg Daily Calories = AVERAGE(FACT_NUTRITION_INTAKE[calories])

Avg Protein Intake = AVERAGE(FACT_NUTRITION_INTAKE[protein_g])

Macro Balance Score = AVERAGE(FACT_NUTRITION_INTAKE[macro_balance_score])
```

#### Time Intelligence

```dax
Workouts MTD = 
CALCULATE(
    [Total Workouts],
    DATESMTD(DIM_DATE[full_date])
)

Workouts YTD = 
CALCULATE(
    [Total Workouts],
    DATESYTD(DIM_DATE[full_date])
)

Workouts Previous Month = 
CALCULATE(
    [Total Workouts],
    DATEADD(DIM_DATE[full_date], -1, MONTH)
)

MoM Growth % = 
DIVIDE(
    [Total Workouts] - [Workouts Previous Month],
    [Workouts Previous Month],
    0
) * 100
```

---

## Design Guidelines

### Color Palette

**Primary Colors:**
- **Brand Blue**: #0078D4 (Headers, primary actions)
- **Success Green**: #107C10 (Positive metrics, growth)
- **Warning Orange**: #FF8C00 (Alerts, attention needed)
- **Error Red**: #D13438 (Critical issues, at-risk)
- **Neutral Gray**: #605E5C (Text, borders)

**Chart Colors:**
- Use consistent colors across dashboards
- Apply conditional formatting for KPIs
- Ensure accessibility (WCAG AA compliance)

### Typography

- **Titles**: Segoe UI Bold, 16pt
- **Subtitles**: Segoe UI Semibold, 12pt
- **Body Text**: Segoe UI Regular, 10pt
- **KPI Values**: Segoe UI Bold, 24pt

### Layout Principles

1. **F-Pattern Reading**: Place most important KPIs top-left
2. **Visual Hierarchy**: Larger visuals for key insights
3. **White Space**: Adequate padding between visuals
4. **Consistent Alignment**: Grid-based layout
5. **Mobile Responsive**: Optimize for tablet/phone viewing

---

## Performance Optimization

### Best Practices

1. **Use Aggregated Tables**: Leverage `AGG_*` tables for summary views
2. **Limit Visual Count**: Maximum 10-12 visuals per page
3. **Optimize DAX**: Use variables, avoid nested CALCULATE
4. **Filter Context**: Apply filters at report level when possible
5. **DirectQuery Optimization**: Enable query folding
6. **Incremental Refresh**: For large fact tables (if using Import mode)

### Query Optimization

```sql
-- Create indexed views in Snowflake for frequently accessed data
CREATE MATERIALIZED VIEW MV_MEMBER_WORKOUT_SUMMARY AS
SELECT 
    member_key,
    workout_date_key,
    COUNT(*) AS workout_count,
    SUM(calories_burned) AS total_calories,
    SUM(duration_minutes) AS total_duration
FROM FACT_WORKOUT_ACTIVITY
GROUP BY member_key, workout_date_key;
```

---

## Implementation Checklist

### Phase 1: Data Connection (Week 1)
- [ ] Configure Snowflake connection in Power BI
- [ ] Import/connect to all required tables
- [ ] Validate data model relationships
- [ ] Test query performance

### Phase 2: Dashboard Development (Week 2-3)
- [ ] Build Executive Overview Dashboard
- [ ] Build Member Analytics Dashboard
- [ ] Build Workout & Nutrition Dashboard
- [ ] Build Operational Insights Dashboard

### Phase 3: DAX & Calculations (Week 3)
- [ ] Create all calculated measures
- [ ] Implement time intelligence functions
- [ ] Add conditional formatting rules
- [ ] Test calculation accuracy

### Phase 4: Design & UX (Week 4)
- [ ] Apply consistent branding
- [ ] Optimize layout and navigation
- [ ] Add drill-through pages
- [ ] Implement bookmarks and tooltips

### Phase 5: Testing & Deployment (Week 5)
- [ ] User acceptance testing
- [ ] Performance testing
- [ ] Security and access control setup
- [ ] Publish to Power BI Service
- [ ] Schedule data refresh (if Import mode)
- [ ] Train end users

---

## Business Impact Metrics

### Expected Outcomes

1. **Reduce Member Churn by 15%**: Early identification of at-risk members
2. **Increase Engagement by 25%**: Personalized recommendations
3. **Optimize Staffing Costs by 10%**: Data-driven scheduling
4. **Improve Member Satisfaction by 20%**: Better facility experience
5. **Increase Revenue by 12%**: Targeted upsell opportunities

### Success Criteria

- Dashboard adoption rate > 80% among management
- Average decision-making time reduced by 40%
- Monthly active users > 50
- User satisfaction score > 4.5/5

---

## Maintenance & Updates

### Regular Tasks

- **Daily**: Monitor data refresh status
- **Weekly**: Review dashboard performance metrics
- **Monthly**: Update KPI targets and thresholds
- **Quarterly**: Gather user feedback and implement improvements
- **Annually**: Comprehensive dashboard redesign review

---

## Conclusion

This Power BI dashboard design provides a comprehensive analytics solution for the Health & Fitness Analytics Platform. By leveraging the star schema data model in Snowflake and implementing best practices in visualization and performance optimization, this dashboard will deliver actionable insights that drive business value and improve member outcomes.

**Next Steps:**
1. Review and approve dashboard design
2. Configure Snowflake connection
3. Begin dashboard development
4. Schedule user training sessions

---

**Document Version Control:**
- v1.0 - Initial design document (December 2025)
