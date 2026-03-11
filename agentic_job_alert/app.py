import streamlit as st
import pandas as pd
from scraper import JobScraper
from storage import JobStore
from agent_logic import JobAgent
from notifier import send_agentic_email_alert
import time
import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Windows-specific asyncio fix for Playwright/Streamlit
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="Agentic Job Alert", layout="wide")

st.title("🤖 Agentic Job Alert System")
st.markdown("Find your dream job with local AI analysis powered by Ollama.")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Ollama Model", ["llama3.2:3b", "llama3.2:1b", "gemma3:4b", "deepseek-r1:1.5b"], index=0)
    search_keywords = st.text_input("LinkedIn Search Keywords", "Python Developer Remote")
    user_prefs = st.text_area("Your Preferences (Natural Language)", 
                             "I am looking for Python developer roles. I prefer remote work or locations in India. I value companies with good technical stacks.")
    
    st.divider()
    st.header("📧 Email Alerts")
    enable_email = st.toggle("Enable Email Notifications", value=False)
    recipient = st.text_input("Your Email Address", 
                             value=os.getenv("EMAIL_ADDRESS", ""), 
                             placeholder="example@gmail.com",
                             help="The email where you want to receive job matches.")
    score_threshold = st.slider("Min AI Score for Email (0-10)", 0.0, 10.0, 6.5,
                               help="Only jobs with a score higher than this will be emailed.")
    
    if st.button("🔔 Test Email Config", use_container_width=True):
        if not recipient:
            st.error("Please enter a recipient email.")
        else:
            with st.spinner("Sending test email..."):
                test_job = {
                    "title": "Test AI Job Position",
                    "company": "AI Agent Corp",
                    "location": "Remote",
                    "link": "https://example.com",
                    "ai_score": 9.5,
                    "ai_analysis": "This is a test notification to verify your email setup."
                }
                if send_agentic_email_alert(recipient, [test_job]):
                    st.success(f"Test email sent to {recipient}!")
                else:
                    st.error("Failed. Check your .env credentials.")

    st.divider()
    
    if st.button("Clear Database"):
        store = JobStore()
        store.clear_jobs()
        st.success("Database cleared!")

# Initialize system
store = JobStore()
scraper = JobScraper(headless=True)
agent = JobAgent(model=model_choice)

# Main Control
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 Start Agentic Search", use_container_width=True):
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_keywords.replace(' ', '%20')}"
        
        with st.status("Agent is working...") as status:
            status.update(label="Scraping LinkedIn...")
            jobs = scraper.scrape_linkedin_jobs(search_url)
            
            if not jobs:
                st.warning("No jobs found. Check your keywords or internet connection.")
            else:
                # Limit to 10 jobs to prevent timeouts
                jobs = jobs[:10]
                status.update(label=f"Analysis started for {len(jobs)} jobs...")
                
                progress_bar = st.progress(0)
                top_jobs = []
                for i, job in enumerate(jobs):
                    status.update(label=f"Analyzing job {i+1}/{len(jobs)}: {job['title']}")
                    score, explanation = agent.analyze_job(job, user_prefs)
                    store.save_job(job, ai_score=score, ai_analysis=explanation)
                    
                    if score >= score_threshold:
                        job_copy = job.copy()
                        job_copy.update({"ai_score": score, "ai_analysis": explanation})
                        top_jobs.append(job_copy)
                        st.sidebar.info(f"✨ Match: {job['title']} ({score}/10)")
                    else:
                        st.sidebar.text(f"  - Skip: {job['title']} ({score}/10)")
                        
                    progress_bar.progress((i + 1) / len(jobs))
                
                if enable_email:
                    if top_jobs:
                        status.update(label="Sending email alerts...")
                        if send_agentic_email_alert(recipient, top_jobs):
                            st.sidebar.success(f"Email sent to {recipient}!")
                            st.toast(f"✅ Email sent with {len(top_jobs)} matches!")
                        else:
                            st.sidebar.error("Failed to send email. Check credentials.")
                            st.error("Email delivery failed. Verify your .env file.")
                    else:
                        st.sidebar.warning("No jobs met your score threshold for email.")
                        st.info(f"ℹ️ {len(jobs)} jobs found, but none scored above {score_threshold}. No email sent.")

                status.update(label="Search complete!", state="complete")
                st.balloons()

# Results Display
st.divider()
st.header("📋 Job Matches")

all_jobs = store.get_all_jobs()
if all_jobs:
    df = pd.DataFrame(all_jobs)
    
    # Custom display
    for _, row in df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(f"{row['title']} @ {row['company']}")
                st.write(f"📍 {row['location']} | 🛡️ Score: **{row['ai_score']}/10**")
                st.info(f"💡 **AI Analysis:** {row['ai_analysis']}")
            with c2:
                st.link_button("View Job", row['link'], use_container_width=True)
else:
    st.info("No jobs found yet. Click 'Start Agentic Search' to begin.")
