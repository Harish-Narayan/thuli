# Thuli Studios Hackathon

## Overview

Thuli Studios is a platform that enables personalized outfit recommendations based on a combination of western celebrity body profiles, user preferences, and wardrobe data from Indian actors. By using advanced AI pipelines such as RAG Fusion and Gemini APIs, the platform ensures accurate recommendations tailored to users' body types and style preferences.
## Architecture
![Copy of Owner Manuals (1)](https://github.com/user-attachments/assets/6b5dd097-d3d9-4728-9922-070e831e6f51)

## Instructions to use:
Generate API Keys for Gemini, QDrant, Cohere and access tokens from HuggingFace. Run:
  ```bash
  python3 controller.py
```
simple streamlit app will be integrated soon....

## User Inputs

The user provides two types of inputs:
1. **Image of a Western Celebrity**  
   An image is uploaded to analyze body features and other important attributes.
   
2. **Custom Semantic Input of Preferences**  
   Example:  
   *"I will be attending a party in Mumbai. The backdrop of the venue is peach-colored. Suggest me some outfits that might fit properly."*

## Pipeline Workflow

1. **Image Processing**  
   - The uploaded image is processed using **Gemini APIs** to extract body features and other relevant details.

2. **RAG Fusion (Body Feature Matching)**  
   - The extracted body features are fused with actor profiles using RAG (Retrieval-Augmented Generation) Fusion.
   - Top 5 Indian celebrities with the most similar body profiles are identified.
   - It is done with help of QDrant VectorDB and Cohere API for generating the embeddings.

3. **Wardrobe Recommendation**  
   - The wardrobes of these 5 celebrities are scanned for outfits that match the user's body type and preferences.
   - Direct outfit recommendations are generated based on the closest matches.

4. **Summarizing Celebrity Profiles**  
   - A summarization step picks out the common body features and outfit choices of the top 5 celebrities.
   - This summary, along with user preferences, is re-fused through another RAG pipeline to create a total wardrobe match.

5. **Final Recommendations**  
   - The results from both pipelines (body profile matching and wardrobe matching) are displayed as existing wardrobe results.

## THULI AI Designer

In addition to recommending existing outfits, **Thuli AI Designer** offers:
- **Custom Outfit Suggestions**:  
  Using the context of western celebrity body types and user preferences, the system compares with similar Indian actor body types and their favorite costumes.
- **Visualization**:  
  The final outfit suggestions are sent to **Stable Diffusion/FLUX** to visualize the results, providing a realistic image of the recommendations.

## Future Improvements

### 1. Data Collection
- Develop custom web crawlers and scrapers for sites like Vogue, Pinterest, and other fashion sources.
- Focus on collecting key features that improve the accuracy of recommendations.

### 2. User Experience
- Build a smooth, immersive user interface (UI) that enhances the overall experience.

### 3. Feature Extraction
- Develop custom **YOLO models** for more precise body feature extraction instead of fully relying on LLMs (Language Learning Models).

### 4. Data Expansion
- Collect a large number of celebrity profiles and wardrobe data to provide more matching opportunities for the RAG Fusion model.

### 5. Decision Pipeline
- Improve the decision-making pipeline to ensure accurate recommendations by considering multiple factors at each stage.

### 6. Designer Templates
- Fix templates for the AI designer and generate realistic images of the suggested outfits.

### 7. Accessories Integration
- Implement solutions to provide accessory recommendations that complement the selected outfits.

---

**Thuli Studios** aims to revolutionize fashion by combining AI-driven insights with personalized recommendations for a unique and tailored experience.
