# 🍽️  Restaurant Name Generator

An AI-powered application that generates **restaurant names, menu items, and taglines** based on user-selected cuisine and food preferences. This project leverages modern LLM capabilities using **LangChain + Groq (LLaMA 3.1)** to create a complete restaurant brand identity in seconds.

---

## 🚀 Features

* 🏷️ Generate **unique restaurant names**
* 🍛 Suggest **5 relevant menu items**
* ✨ Create **catchy brand taglines**
* 🎯 Supports multiple cuisines (Indian, Italian, Japanese, etc.)
* 🥗 Customizable food preference (Veg / Non-Veg / Both)
* ⚡ Fast inference using Groq (LLaMA 3.1)

---

## 🧠 How It Works

The application uses **prompt chaining with LangChain**:

1. Generate restaurant name based on cuisine
2. Generate menu items using the restaurant name
3. Generate a tagline for branding

Each step is powered by an LLM and connected using LangChain pipelines.

Core logic example:

```python
restaurant_name = (prompt1 | llm).invoke({"cuisine": cuisine}).content.strip()
food_items = (prompt2 | llm).invoke({
    "restaurant_name": restaurant_name,
    "food_type": food_type
}).content
tagline = (prompt3 | llm).invoke({"restaurant_name": restaurant_name}).content.strip()
```

📄 Full UI implementation available here: 

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (UI)
* **LangChain (LCEL / Runnables)**
* **Groq API (LLaMA 3.1)**
* **dotenv**

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/restaurant-name-generator.git
cd restaurant-name-generator
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📸 Output Example

* Restaurant Name: *Spice Symphony*
* Menu Items:

  * Paneer Tikka
  * Butter Naan
  * Dal Makhani
  * Veg Biryani
  * Gulab Jamun
* Tagline: *Where flavors meet harmony*

---

## ⚠️ Important Notes

* Do **NOT push `.env` file** to GitHub
* Keep your API keys secure
* Add `.env` to `.gitignore`

---

## 💡 Future Improvements

* 🔥 Add multi-agent system
* 🧠 Add memory-based recommendations
* 🌐 Convert into FastAPI backend
* 🎨 Enhance UI/UX further
* 📊 Add analytics & feedback loop

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 👨‍💻 Author

**Ashish Jadhav**
Aspiring AI / ML Engineer

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and support the work!
