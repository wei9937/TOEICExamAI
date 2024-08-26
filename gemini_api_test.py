import google.generativeai as genai
import os

api_key = 'AIzaSyA0l5znOw4cYHL_kBqLxd81OVq3T_cZFj4'
genai.configure(api_key = api_key)

model = genai.GenerativeModel('gemini-pro')

prompt_text = """
請生成十題多益考題Part5（句子填空），包括以下內容：
1. 一個句子，其中有一個或多個空格供填寫。
2. 四個選項，其中只有一個是正確的。
3. 題目應該涵蓋文法題、單字題、詞性變化和時態題等多益考試可能會出的題型。
4. 正確答案和每題的詳解。

請將題目和答案分開顯示，格式如下：

題目區：
1. **題目** 1: [句子內容，其中有一個或多個空格]
   - A. [選項A]
   - B. [選項B]
   - C. [選項C]
   - D. [選項D]

2. **題目** 2: [句子內容，其中有一個或多個空格]
   - A. [選項A]
   - B. [選項B]
   - C. [選項C]
   - D. [選項D]

...

答案區：
1. 題目1的答案: [正確答案選項]
   題目1的詳解: [詳解內容，解釋為什麼為這答案，若是考詞性變化的題型，請說明各答案的詞性]

2. 題目2的答案: [正確答案選項]
   題目2的詳解: [詳解內容]
"""

response = model.generate_content(prompt_text)
print(response.text)
