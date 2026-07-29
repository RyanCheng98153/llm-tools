import os
import json
from typing import List, Optional, Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI
from langfuse import Langfuse, observe

# 1. 環境設定
load_dotenv()

# 初始化 OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 初始化 Langfuse (Self-hosted)
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# 2. 定義 Pydantic 資料模型
class Ingredient(BaseModel):
    name: str
    amount: str

class Recipe(BaseModel):
    difficulty: str = Field(description="easy / medium / hard")
    ingredients: List[Ingredient]
    steps: List[str]
    time_minutes: int
    comment: str

# 3. 通用的 LLM Generation Function
@observe()
def llm_generation(
    messages: list,
    model_name: str = "gpt-5.4-nano",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    response_model: Optional[Type[BaseModel]] = None
):
    """
    通用的 LLM 生成函數。
    如果提供 response_model 且模型支援，則使用 Structured Outputs。
    """
    
    # 判斷是否要使用 response_format (OpenAI 的 parse 方法會自動處理)
    if response_model:
        # 使用 beta.chat.completions.parse 直接支援 Pydantic
        completion = client.beta.chat.completions.parse(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_model,
        )
        return completion.choices[0].message.parsed
    else:
        # 一般生成
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content

# 4. 料理 Agent 邏輯
@observe()
def recipe_agent(food_name: str):
    messages = [
        {"role": "system", "content": "You are a professional chef. Provide a recipe for the requested food."},
        {"role": "user", "content": f"I want to eat: {food_name}"}
    ]
    
    # 調用通用的 llm_generation
    recipe_data = llm_generation(
        messages=messages,
        model_name="gpt-4o-mini", # 或 gpt-4o 等支援格式化輸出的模型
        response_model=Recipe
    )
    
    # 儲存到 ./output/ 資料夾
    if not os.path.exists("./output"):
        os.makedirs("./output")
        
    file_path = f"./output/{food_name.replace(' ', '_')}.json"
    
    # 將 Pydantic Model 轉為 dict 並存檔
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(recipe_data.model_dump(), f, indent=4, ensure_ascii=False)
        
    return recipe_data

# 5. Main function 互動介面
def main():
    print("Chef Agent is ready! (Type 'exit' to quit)")
    
    while True:
        user_input = input("\nWhat do you like to eat today? ")
        
        if user_input.lower() in ["exit", "quit", "離開"]:
            break
            
        try:
            # 執行 Agent 並追蹤
            print(f"Cooking up a recipe for {user_input}...")
            recipe = recipe_agent(user_input)
            
            # 輸出結果
            print("\n--- Recipe Result ---")
            print(f"Difficulty: {recipe.difficulty}")
            print(f"Time: {recipe.time_minutes} mins")
            print(f"Ingredients: {', '.join([f'{i.name}({i.amount})' for i in recipe.ingredients])}")
            print(f"Steps: {recipe.steps[0]}...") # 只印出第一步作為範例
            print(f"Comment: {recipe.comment}")
            print(f"--- Saved to ./output/{user_input}.json ---")
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()