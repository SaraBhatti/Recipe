import streamlit as st
import requests
import json

# Function to search for recipes using the Edamam API
def recipe_search(ingredient, app_id, app_key):
    url = f"https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}"
    response = requests.get(url)
    data = response.json()

    if 'hits' in data:
        return data['hits']
    else:
        return []

# Function to save the search results to a file
def save_to_file(recipes, ingredient):
    filename = f"{ingredient}_recipes.txt"
    with open(filename, "w") as f:
        for result in recipes:
            recipe = result['recipe']
            f.write(f"Recipe Name: {recipe['label']}\n")
            f.write(f"Recipe URL: {recipe['url']}\n")
            f.write(f"Calories: {recipe['calories']:.2f}\n")
            if 'cuisineType' in recipe:
                f.write(f"Cuisine: {', '.join(recipe['cuisineType'])}\n")
            f.write("\n")
    st.success(f"Results saved to {filename}")

# Streamlit app
def main():
    # Title and description
    st.title("Recipe Finder")
    st.write("Search for recipes based on an ingredient using the Edamam API.")
    
    # Input for ingredient
    ingredient = st.text_input("Enter an ingredient", "chicken")

    # API Credentials (these should be your own App ID and Key)
    app_id = '9abc9f35'
    app_key = '69f933f2cd59a612e81884cd1478f3da'

    # Input for low-calorie preference
    low_calorie = st.checkbox("Low-calorie recipes (≤ 500 calories)")
    
    # Input for cuisine filter
    cuisine = st.text_input("Filter by cuisine type (optional)", "")
    
    # Button to search for recipes
    if st.button("Search Recipes"):
        # Get the search results
        results = recipe_search(ingredient, app_id, app_key)
        
        # Sort by calories and filter by preferences
        if results:
            results_sorted = sorted(results, key=lambda x: x['recipe']['calories'])

            filtered_results = []
            for result in results_sorted:
                recipe = result['recipe']
                # Filter low-calorie recipes
                if low_calorie and recipe['calories'] > 500:
                    continue
                # Filter by cuisine type
                if cuisine and cuisine.lower() not in (c.lower() for c in recipe.get('cuisineType', [])):
                    continue
                filtered_results.append(result)
            
            # Display results
            if filtered_results:
                st.write(f"Recipes with {ingredient}:")

                for result in filtered_results:
                    recipe = result['recipe']
                    st.subheader(recipe['label'])
                    st.write(f"Cuisine: {', '.join(recipe.get('cuisineType', ['Unknown']))}")
                    st.write(f"Calories: {recipe['calories']:.2f}")
                    st.write(f"[View Recipe]({recipe['url']})")
                    st.write("---")

                # Option to save results to a file
                if st.button("Save Results to File"):
                    save_to_file(filtered_results, ingredient)
            else:
                st.warning("No recipes found with the specified preferences.")
        else:
            st.error("No recipes found for this ingredient.")
    
# Run the app
if __name__ == "__main__":
    main()
