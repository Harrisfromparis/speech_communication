import os
import random
from pathlib import Path

import openai
import streamlit as st
import streamlit.components.v1 as components
from dotenv import find_dotenv, load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch

# Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent
PDF_FILE_PATH = BASE_DIR / "pdf.pdf"
SPEAKIFY_TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"

# Set page configuration
st.set_page_config(page_title="Let's Talk", page_icon="🗣️", layout="wide")

# Sidebar for navigation
st.sidebar.title("Let's Talk")
page = st.sidebar.selectbox(
    "Select a page:",
    ["Chatbot", "Speakify", "Community", "Resources", "Activities"],
)


@st.cache_resource(ttl="1h")
def configure_qa_chain(pdf_file_path):
    loader = PyPDFLoader(str(pdf_file_path))
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2, "fetch_k": 4})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=openai.api_key,
        streaming=True,
    )

    return ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory,
        verbose=True,
    )


@st.cache_data
def load_speakify_app():
    return SPEAKIFY_TEMPLATE_PATH.read_text(encoding="utf-8")


qa_chain = configure_qa_chain(PDF_FILE_PATH)


if page == "Chatbot":
    st.title("🗣️ Let's Talk")
    st.markdown(
        "Welcome to Let's Talk. I’m here to share support, resources, and guidance for speech communication."
    )

    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hello! How can I assist you today?"}
        ]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query = st.chat_input(
        placeholder="Ask anything about speech communication or therapy..."
    )

    if user_query:
        st.session_state["messages"].append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            response = qa_chain.run(user_query)
            st.session_state["messages"].append(
                {"role": "assistant", "content": response}
            )
            st.write(response)

    with st.expander("About Let's Talk", expanded=False):
        st.markdown(
            "Let's Talk provides speech support resources, guided conversations, and practice tools in one place."
        )

elif page == "Speakify":
    st.title("🎙️ Speakify Practice")
    st.markdown(
        "Use Speakify to hear a prompt, speak it aloud, and compare your words with the target phrase."
    )
    components.html(load_speakify_app(), height=760, scrolling=False)

    with st.expander("How Speakify helps", expanded=False):
        st.markdown(
            """
            - Listen to short prompts with text-to-speech.
            - Practice speaking with your device microphone.
            - Review the live transcript and try again when needed.
            """
        )

elif page == "Community":
    st.title("💬 Let's Talk Community")
    st.markdown("Share your experiences or thoughts about communication support below:")

    if "community_thoughts" not in st.session_state:
        st.session_state["community_thoughts"] = []

    community_input = st.text_area(
        "Your thoughts:", placeholder="Type your thoughts here..."
    )

    if st.button("Submit"):
        if community_input:
            st.session_state["community_thoughts"].append(community_input)
            st.success("Thank you for sharing your thoughts!")
        else:
            st.warning("Please enter a message before submitting.")

    st.markdown("### Shared thoughts")
    for thought in st.session_state["community_thoughts"]:
        st.markdown(f"- {thought}")

    with st.expander("Contact", expanded=False):
        st.markdown(
            "For more information, contact Let's Talk at support@letstalk.app or +1 (800) 123-4567."
        )

elif page == "Resources":
    st.title("📚 Let's Talk Resources")
    st.markdown(
        """
        Here are some resources and tips that can support speech communication practice:

        ### Useful Links:
        - [American Speech-Language-Hearing Association (ASHA)](https://www.asha.org)
        - [SpeechPathology.com](https://www.speechpathology.com)
        - [National Stuttering Association](https://westutter.org)

        ### Tips for Improving Speech:
        1. **Practice regularly**: Build a short daily routine.
        2. **Record yourself**: Replay your speech and notice patterns.
        3. **Use visual aids**: Pair sounds with pictures and prompts.
        4. **Stay patient**: Celebrate gradual progress.

        ### Books and Materials:
        - *The Complete Handbook of Speech and Language Therapy* by Sheila D. Johnson
        - *Talkability: 8 Steps to Teaching Your Child to Communicate* by Fern Sussman

        ### Support Groups:
        - Join local or online groups to learn from people on similar journeys.
        """
    )

elif page == "Activities":
    st.title("🎯 Let's Talk Activities")
    st.markdown(
        """
        Explore quick activities designed to strengthen speech skills.

        ### Word Puzzle:
        Guess the word from the definition below.
        """
    )

    word_definitions = {
        "Articulation": "The clear and precise pronunciation of words.",
        "Fluency": "The smoothness or flow with which sounds, syllables, words, and phrases are joined together.",
        "Stuttering": "A speech disorder that involves frequent and significant disruptions in the normal flow of speech.",
        "Phoneme": "The smallest unit of sound in speech.",
        "Language": "A system of communication used by a particular community or country.",
    }

    word, definition = random.choice(list(word_definitions.items()))
    st.markdown(f"**Definition:** {definition}")

    user_guess = st.text_input("Your guess:", placeholder="Type your answer here...")

    if st.button("Submit Guess"):
        if user_guess.lower() == word.lower():
            st.success("Correct! 🎉 The word is: " + word)
        else:
            st.error("Incorrect! 😢 Try again.")

    if st.button("Reveal Answer"):
        st.info(f"The word was: {word}")


st.sidebar.markdown("### Join the conversation")
st.sidebar.markdown("- Chat with the support assistant")
st.sidebar.markdown("- Practice aloud with Speakify")
st.sidebar.markdown("- Share with the community")
