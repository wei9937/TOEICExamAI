import tkinter as tk
from tkinter import ttk, messagebox

# 創建主窗口
root = tk.Tk()
root.title("AI 多益測驗")
root.geometry("800x800")  # 設置固定窗口大小

# 創建 Canvas 和 Scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# 滾動內容框架
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# 將框架添加到 Canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.config(yscrollcommand=scrollbar.set)

def on_mouse_wheel(event):
    if event.num == 4 or event.delta > 0:  # 向上滾動
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:  # 向下滾動
        canvas.yview_scroll(1, "units")

root.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows 和 macOS
# root.bind_all("<Button-4>", on_mouse_wheel)  # Linux 向上滾動
# root.bind_all("<Button-5>", on_mouse_wheel)  # Linux 向下滾動

def show_main_menu():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    tk.Label(scrollable_frame, text="選擇考題單元").pack(pady=10)
    
    tk.Button(scrollable_frame, text="Part 5 句子填空", command=lambda: show_questions("Part 5")).pack(pady=5)
    tk.Button(scrollable_frame, text="Part 6 段落填空", command=lambda: show_questions("Part 6")).pack(pady=5)
    tk.Button(scrollable_frame, text="Part 7 閱讀測驗", command=lambda: show_questions("Part 7")).pack(pady=5)

def show_questions(unit):
    # 清除之前的內容
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # 添加主選單按鈕
    tk.Button(scrollable_frame, text="主選單", command=show_main_menu).pack(pady=10)

    # 顯示選定單元的考題（示範代碼）
    questions = [f"Question {i+1} for {unit}" for i in range(10)]  # 模擬考題
    
    # 顯示考題和選項
    for i, question in enumerate(questions):
        tk.Label(scrollable_frame, text=question).pack(anchor="w", padx=10, pady=5)
        for option in ["A", "B", "C", "D"]:
            rb = tk.Radiobutton(scrollable_frame, text=f"Option {option}", value=option)
            rb.pack(anchor="w", padx=20)
    
    # 添加送出按鈕
    submit_button = tk.Button(scrollable_frame, text="送出答案", command=submit_answers)
    submit_button.pack(pady=20)

def submit_answers():
    messagebox.showinfo("提交", "答案已提交！")

# 初始化顯示主選單
show_main_menu()

root.mainloop()
