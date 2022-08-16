"""
Language Translation using Argostranslate
"""


# Imports
import streamlit as st
import argostranslate.package, argostranslate.translate


# Functions
@st.cache
def get_available_translation_pairs():
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    return available_packages


@st.cache
def get_translation_model(source_language, target_language, available_packages):
    available_package = list(
        filter(
            lambda x: x.from_code == source_language and x.to_code == target_language, available_packages
        )
    )[0]
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)


@st.cache
def get_translation(text, source_language, target_language):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
        lambda x: x.code == source_language,
        installed_languages))[0]
    to_lang = list(filter(
        lambda x: x.code == target_language,
        installed_languages))[0]
    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(str(text))
    return translated_text


# Main App
"""
# KrisNLP Language Translation
"""
available_packages = get_available_translation_pairs()
if st.checkbox("Show available translation pairs"):
    st.write(available_packages)

col1, col2 = st.columns(2)
with col1:
    source_language_code = st.text_input("Enter source language code:", "en")
with col2:
    target_language_code = st.text_input("Enter target language code:", "es")

with st.spinner("Loading translation model..."):
    try:
        get_translation_model(source_language_code, target_language_code, available_packages)
    except IndexError:
        st.write("Unsupported language code")
        st.stop()

text2translate = st.text_area("Enter text to translate:", "Singapore Airlines is the best airline in the world!")
with st.spinner("Translating..."):
    translated_text = get_translation(text2translate, source_language_code, target_language_code)
st.write(translated_text)
