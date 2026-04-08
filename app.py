import streamlit as st
from groq import Groq
from tavily import TavilyClient

# --- INITIALIZATION ---
st.set_page_config(page_title="ViralVision AI", page_icon="🎬", layout="wide")

if not st.secrets:
    st.error("🚫 No secrets found at all. Check your .streamlit folder location.")
    st.stop()

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    TAVILY_KEY = st.secrets["TAVILY_API_KEY"]
except KeyError as e:
    st.error(f"❌ Key {e} not found in secrets.toml! Check your spelling.")
    st.stop()

groq_client = Groq(api_key=GROQ_KEY)
tavily_client = TavilyClient(api_key=TAVILY_KEY)


st.title(" Viral SM:  Trending Content Hunter")
st.markdown("Generate a viral blueprint based on real-time controversies and trending hits.")

if st.button("Generate Viral Content"):
    with st.spinner("Scanning Social Media & Live Web Data..."):
        # 1. YOUR ORIGINAL SEARCH QUERY
        search_query = "trending songs Instagram , top social media influencers, actors , tiktokers and their viral controversies, viral YouTube controversy videos or movies, hit trending songs from pakistan and india region specifically this week"
        
        try:
            search_result = tavily_client.search(query=search_query, search_depth="advanced", max_results=10)
            context = str(search_result['results'])

            # 2. YOUR ORIGINAL PROMPT (UNTOUCHED)
            prompt = f"""
            Using this LIVE WEB DATA: {context}
            
            Act as a Content Architect for a new creator. u have to choose india and pakistan region for depth search Provide a 'Viral Blueprint' for April 2026:
            1. **MUSIC:** List 5 trending movies songs for Reels/TikTok.
            2. **STARS:** Mention social media  influencers are in hot discussion due to any controversy or conflict in Pakistan or India
            3. **Controversies:** What is the #1 viral controversial hit movie or any talk show or any fight between youtuber or tiktokers belongs to Pakistan and India.
            4. **IDEA:** Give a 1-sentence video idea for youtube short or video related to Pakistan and India Region   that can get views easily without getting paid views .
            
            Format it cleanly for a professional portfolio.
            """

            # 3. GROQ EXECUTION
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # 4. DISPLAY RESULTS
            st.success("Analysis Complete!")
            st.markdown("---")
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.sidebar.info("This tool uses real-time data from Tavily and Groq Llama 3.1.")