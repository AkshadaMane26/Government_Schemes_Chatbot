#!/bin/bash

cat << 'EOF' > README.md
# PolicyGuide 🗺️ – Chatbot for Government Schemes

**PolicyGuide** is an intelligent chatbot designed to help users navigate Indian Government Schemes related to **Farmers**, **Education**, **Healthcare**, and **Women Empowerment**. It uses Natural Language Processing (NLP) and Machine Learning to understand user queries and respond with accurate information collected from verified government sources.

## 🔍 Features

- Multi-domain chatbot interface:
  - 🧑‍🌾 Farmer
  - 🎓 Education
  - 🏥 Healthcare
  - 👩 Women Welfare
- Data collected from authentic government websites and structured into `.json` files
- Trained using **Logistic Regression** and **TF-IDF vectorization**
- Django-based web frontend for category-wise interactions
- Modular architecture with separate models for each category

## 📁 Project Structure

