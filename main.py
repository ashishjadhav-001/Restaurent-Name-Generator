
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

# =========================
# Prompt Templates
# =========================

prompt1 = PromptTemplate.from_template(
    "Suggest ONE fancy name for a {cuisine} restaurant. Only return the name."
)

prompt2 = PromptTemplate.from_template(
    """
Suggest exactly 5 popular {food_type} food items for a restaurant named {restaurant_name}.

Rules:
- Only return the list
- No extra sentence

Format:
1. item
2. item
3. item
4. item
5. item
"""
)

prompt3 = PromptTemplate.from_template(
    "Write ONE short catchy tagline for a restaurant named {restaurant_name}. Only return the tagline."
)


# =========================
# Main Function
# =========================
def generate_restaurant(cuisine, food_type):
    try:
        # Generate restaurant name
        restaurant_name = (prompt1 | llm).invoke({
            "cuisine": cuisine
        }).content.strip()

        # Generate food items
        food_items_raw = (prompt2 | llm).invoke({
            "restaurant_name": restaurant_name,
            "food_type": food_type
        }).content

        # Generate tagline
        tagline = (prompt3 | llm).invoke({
            "restaurant_name": restaurant_name
        }).content.strip()

        # Clean tagline
        tagline = tagline.replace('"', '').strip()

        # Clean food items
        food_items = []
        for item in food_items_raw.split("\n"):
            item = item.strip()

            if item and "here are" not in item.lower():
                if "." in item:
                    item = item.split(".", 1)[1].strip()
                food_items.append(item)

        return {
            "restaurant_name": restaurant_name,
            "food_items": food_items,
            "tagline": tagline
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# Example Usage
# =========================
if __name__ == "__main__":
    result = generate_restaurant("Indian", "Veg")

    if "error" in result:
        print("❌ Error:", result["error"])
    else:
        print("\n🍴 Restaurant Name:", result["restaurant_name"])
        print("\n🍛 Food Items:")
        for item in result["food_items"]:
            print("-", item)
        print("\n✨ Tagline:", result["tagline"])