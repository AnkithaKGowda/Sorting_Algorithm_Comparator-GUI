import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Sorting Algorithms ---------------- #

def bubble_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        for j in range(len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def selection_sort(arr):
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

def quick_sort(arr):
    a = arr.copy()
    def partition(left, right):
        pivot = a[left]
        l = left + 1
        r = right
        while l <= r:
            while l <= right and a[l] <= pivot:
                l += 1
            while a[r] > pivot:
                r -= 1
            if l < r:
                a[l], a[r] = a[r], a[l]
        a[left], a[r] = a[r], a[left]
        return r
    
    def quick(left, right):
        if left < right:
            loc = partition(left, right)
            quick(left, loc - 1)
            quick(loc + 1, right)
    
    quick(0, len(a) - 1)
    return a

def quick_sort_metrics(arr):
    m = Metrics()
    a = arr.copy()
    def partition(left, right):
        pivot = a[left]
        l = left + 1
        r = right
        while l <= r:
            while l <= right and a[l] <= pivot:
                m.comparisons += 1
                l += 1
            while a[r] > pivot:
                m.comparisons += 1
                r -= 1
            if l < r:
                a[l], a[r] = a[r], a[l]
                m.swaps += 1
        a[left], a[r] = a[r], a[left]
        m.swaps += 1
        return r
    
    def quick(left, right):
        if left < right:
            loc = partition(left, right)
            quick(left, loc - 1)
            quick(loc + 1, right)
    
    quick(0, len(a) - 1)
    return a, m

# ---------------- Step Visualizers ---------------- #

def bubble_sort_steps(arr):
    a = arr.copy()
    steps = []
    for i in range(len(a)):
        for j in range(len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                steps.append((a.copy(), "Swapped adjacent elements"))
    return steps

def insertion_sort_steps(arr):
    a = arr.copy()
    steps = []
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j+1] = a[j]
            j -= 1
            steps.append((a.copy(), "Shifted element right"))
        a[j+1] = key
        steps.append((a.copy(), "Inserted element in correct position"))
    return steps

def selection_sort_steps(arr):
    a = arr.copy()
    steps = []
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
        steps.append((a.copy(), f"Placed minimum at position {i}"))
    return steps

def merge_sort_steps(arr):
    steps = []
    def merge_internal(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i]); i+=1
            else:
                result.append(right[j]); j+=1
        result += left[i:] + right[j:]
        steps.append((result.copy(), "Merged two sorted halves"))
        return result

    def merge_sort_internal(a):
        if len(a) <= 1:
            return a
        mid = len(a)//2
        left = merge_sort_internal(a[:mid])
        right = merge_sort_internal(a[mid:])
        return merge_internal(left, right)

    merge_sort_internal(arr.copy())
    return steps

def quick_sort_steps(arr):
    a = arr.copy()
    steps = []
    
    def partition(left, right, depth):
        pivot = a[left]
        l = left + 1
        r = right
        steps.append((a.copy(), f"[Depth {depth}] Pivot = {pivot} at index {left}"))
        
        swap_count = 0
        while l <= r:
            while l <= right and a[l] <= pivot:
                l += 1
            while a[r] > pivot:
                r -= 1
            if l < r:
                a[l], a[r] = a[r], a[l]
                swap_count += 1
                steps.append((a.copy(), f"[Depth {depth}] Swapped elements → {a}"))
        
        a[left], a[r] = a[r], a[left]
        steps.append((a.copy(), f"[Depth {depth}] Placed pivot {pivot} at correct position {r}"))
        return r
    
    def quick(left, right, depth=0):
        if left < right:
            loc = partition(left, right, depth)
            quick(left, loc - 1, depth + 1)
            quick(loc + 1, right, depth + 1)
    
    quick(0, len(a) - 1)
    return steps

# ---------------- Metrics ---------------- #

class Metrics:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

def bubble_sort_metrics(arr):
    m = Metrics()
    a = arr.copy()
    for i in range(len(a)):
        for j in range(len(a)-i-1):
            m.comparisons += 1
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                m.swaps += 1
    return a, m

def insertion_sort_metrics(arr):
    m = Metrics()
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            m.comparisons += 1
            if key < a[j]:
                a[j+1] = a[j]
                m.swaps += 1
                j -= 1
            else:
                break
        a[j+1] = key
    return a, m

def selection_sort_metrics(arr):
    m = Metrics()
    a = arr.copy()
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            m.comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            m.swaps += 1
    return a, m

# ---------------- Input Analysis ---------------- #

def detect_input_type(arr):
    if arr == sorted(arr):
        return "Sorted"
    elif arr == sorted(arr, reverse=True):
        return "Reverse Sorted"
    else:
        return "Random"

def suggest_best(arr):
    if arr == sorted(arr):
        return "Insertion (Best Case)"
    elif arr == sorted(arr, reverse=True):
        return "Merge (Avoid Worst Case)"
    elif len(arr) < 20:
        return "Insertion (Small Input)"
    else:
        return "Quick (Fast Average)"

# ---------------- Complexity ---------------- #

complexity_data = {
    "Bubble": ("O(n)", "O(n²)", "O(n²)"),
    "Insertion": ("O(n)", "O(n²)", "O(n²)"),
    "Selection": ("O(n²)", "O(n²)", "O(n²)"),
    "Merge": ("O(n log n)", "O(n log n)", "O(n log n)"),
    "Quick": ("O(n log n)", "O(n log n)", "O(n²)")
}

# ---------------- GUI ---------------- #

class SortApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x750")

        BIG = ("Arial", 14)

        tk.Label(root, text="Sorting Algorithm Comparator",
                 font=("Segoe UI", 20, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Enter Numbers:", font=BIG).grid(row=0, column=0)
        self.input_box = tk.Entry(frame, width=40, font=BIG)
        self.input_box.grid(row=0, column=1)

        tk.Button(frame, text="Generate Random", font=BIG,
                  command=self.generate_random).grid(row=0, column=2)

        tk.Label(frame, text="Size:", font=BIG).grid(row=1, column=0)
        self.size_entry = tk.Entry(frame, font=BIG)
        self.size_entry.grid(row=1, column=1)

        tk.Button(frame, text="Run", font=BIG, bg="#4DC179", fg="white",
                  command=self.run).grid(row=1, column=2, padx=100)

        # Row 2: Show Steps and Compare combined
        # Show Steps section
        tk.Label(frame, text="Show Steps:", font=("Arial", 10)).grid(row=2, column=0, padx=2)
        self.algo_choice = ttk.Combobox(frame,
            values=["Bubble","Insertion","Selection","Merge","Quick"], width=9, state="readonly")
        self.algo_choice.bind("<<ComboboxSelected>>", lambda e: self.show_steps())
        self.algo_choice.grid(row=2, column=1, padx=2)

        # Compare section (reduced space)
        tk.Label(frame, text="Compare:", font=("Arial", 10)).grid(row=2, column=2, padx=2)
        self.algo_choice1 = ttk.Combobox(frame,
            values=["Bubble","Insertion","Selection","Merge","Quick"], width=9, state="readonly")
        self.algo_choice1.grid(row=2, column=3, padx=2)
        
        tk.Label(frame, text="vs", font=("Arial", 10, "bold")).grid(row=2, column=4, padx=2)
        
        self.algo_choice2 = ttk.Combobox(frame,
            values=["Bubble","Insertion","Selection","Merge","Quick"], width=9, state="readonly")
        self.algo_choice2.grid(row=2, column=5, padx=2)

        tk.Button(frame, text="Display", font=("Arial", 10, "bold"),
                  command=self.compare_algorithms, bg="#4ECDC4", fg="white", width=8).grid(row=2, column=6, padx=2)

        self.output = tk.Text(root, height=12, font=("Courier", 12))
        self.output.pack(fill="x", pady=10)

        # Container for table + graph (side by side)
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        # Graph on LEFT (more space)
        self.graph_frame = tk.Frame(container)
        self.graph_frame.pack(side="left", fill="both", expand=True)

        # Table on RIGHT (compact)
        table_frame = tk.Frame(container)
        table_frame.pack(side="right", fill="y", padx=10)

        # Configure style for larger font
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        # Reduced table height
        self.tree = ttk.Treeview(table_frame,
            columns=("Algo", "Best", "Avg", "Worst"),
            show="headings", height=6, style="Treeview")

        self.tree.column("Algo", width=110)
        self.tree.column("Best", width=90)
        self.tree.column("Avg", width=90)
        self.tree.column("Worst", width=90)

        self.tree.heading("Algo", text="Algorithm")
        self.tree.heading("Best", text="Best")
        self.tree.heading("Avg", text="Average")
        self.tree.heading("Worst", text="Worst")

        self.tree.pack(side="top", fill="both", expand=True, padx=5, pady=10)

    def generate_random(self):
        n = int(self.size_entry.get() or 10)
        arr = [random.randint(0,100) for _ in range(n)]
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, ",".join(map(str, arr)))

    def parse_input(self):
        try:
            return list(map(int, self.input_box.get().split(",")))
        except:
            return []

    def measure(self, func, arr, use_metrics=False):
        start = time.time()
        if use_metrics:
            sorted_arr, metrics = func(arr.copy())
        else:
            sorted_arr = func(arr.copy())
            metrics = Metrics()
        return sorted_arr, time.time()-start, metrics

    def run(self):
        self.output.delete(1.0, tk.END)

        arr = self.parse_input()
        if not arr:
            self.output.insert(tk.END, "Invalid Input!\n")
            return

        self.output.insert(tk.END,
            f"Detected: {detect_input_type(arr)}\n")
        self.output.insert(tk.END,
            f"Suggested: {suggest_best(arr)}\n\n")

        algos = {
            "Bubble": (bubble_sort_metrics, True),
            "Insertion": (insertion_sort_metrics, True),
            "Selection": (selection_sort_metrics, True),
            "Merge": (merge_sort, False),
            "Quick": (quick_sort_metrics, True)
        }

        results = {}

        for name,(f,mflag) in algos.items():
            s,tm,m = self.measure(f,arr,mflag)
            results[name]=tm
            eff = 1/(tm+1e-6)

            self.output.insert(tk.END,
                f"\n{name} Algorithm\n" + "-"*30 + "\n")
            self.output.insert(tk.END, f"Sorted: {s}\n")
            self.output.insert(tk.END, f"Time: {tm:.6f}\n")
            self.output.insert(tk.END, f"Comparisons: {m.comparisons}\n")
            self.output.insert(tk.END, f"Swaps: {m.swaps}\n")
            self.output.insert(tk.END, f"Efficiency: {eff:.2f}\n")

        self.show_table()
        self.plot(results)

    def show_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for algo,vals in complexity_data.items():
            self.tree.insert("", "end", values=(algo,*vals))

    def plot(self, results):
        for w in self.graph_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(results.keys(), results.values())
        ax.ticklabel_format(style='plain', axis='y')
        ax.set_title("Execution Time Comparison")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_steps(self):
        arr = self.parse_input()
        algo = self.algo_choice.get()

        mapping = {
            "Bubble": bubble_sort_steps,
            "Insertion": insertion_sort_steps,
            "Selection": selection_sort_steps,
            "Merge": merge_sort_steps,
            "Quick": quick_sort_steps
        }

        steps = mapping[algo](arr)

        explanations = {
            "Bubble": "Compares adjacent elements and swaps them.",
            "Insertion": "Places each element into its correct position.",
            "Selection": "Selects smallest element and places it first.",
            "Merge": "Divides array and merges sorted halves.",
            "Quick": "Partitions array using pivot."
        }

        win = tk.Toplevel(self.root)
        win.title("Step Visualizer")

        text = tk.Text(win, font=("Courier", 12))
        text.pack(fill="both", expand=True)

        text.insert(tk.END,
            f"{algo} Sort:\n{explanations[algo]}\n\n")

        for i,(step,desc) in enumerate(steps):
            text.insert(tk.END,
                f"Step {i+1}: {step}\n→ {desc}\n\n")

        tk.Button(win, text="Back",
                  command=win.destroy).pack()

    def compare_algorithms(self):
        arr = self.parse_input()
        if not arr:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "Invalid Input!\n")
            return

        algo1 = self.algo_choice1.get()
        algo2 = self.algo_choice2.get()

        if not algo1 or not algo2:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "Select two algorithms to compare!\n")
            return

        # Create comparison window
        comp_win = tk.Toplevel(self.root)
        comp_win.title(f"Side-by-Side: {algo1} vs {algo2}")
        comp_win.geometry("1200x600")

        # Main frame for graphs
        graph_container = tk.Frame(comp_win)
        graph_container.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT GRAPH - Algorithm 1
        left_frame = tk.Frame(graph_container)
        left_frame.pack(side="left", fill="both", expand=True)

        tk.Label(left_frame, text=algo1, font=("Arial", 16, "bold")).pack(pady=5)
        left_graph_frame = tk.Frame(left_frame)
        left_graph_frame.pack(fill="both", expand=True)

        # RIGHT GRAPH - Algorithm 2
        right_frame = tk.Frame(graph_container)
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text=algo2, font=("Arial", 16, "bold")).pack(pady=5)
        right_graph_frame = tk.Frame(right_frame)
        right_graph_frame.pack(fill="both", expand=True)

        # Algorithm mapping
        algos = {
            "Bubble": (bubble_sort_metrics, True),
            "Insertion": (insertion_sort_metrics, True),
            "Selection": (selection_sort_metrics, True),
            "Merge": (merge_sort, False),
            "Quick": (quick_sort_metrics, True)
        }

        # Get functions and flags
        func1, use_metrics1 = algos[algo1]
        func2, use_metrics2 = algos[algo2]

        sorted1, time1, metrics1 = self.measure(func1, arr, use_metrics1)
        sorted2, time2, metrics2 = self.measure(func2, arr, use_metrics2)

        # Create comparison data
        comparison_data = {
            algo1: time1,
            algo2: time2
        }

        # Determine colors based on speed (Green=Faster, Red=Slower)
        if time1 < time2:
            color1 = '#27AE60'  # Green - faster
            color2 = '#E74C3C'  # Red - slower
        elif time2 < time1:
            color1 = '#E74C3C'  # Red - slower
            color2 = '#27AE60'  # Green - faster
        else:
            color1 = '#F39C12'  # Orange - equal
            color2 = '#F39C12'  # Orange - equal

        # Helper function for animated bars
        def animate_bar(ax, bar, target_height, label_text, duration_ms=800):
            """Animate bar growth"""
            start_time = time.time()
            start_height = 0
            
            def update_bar():
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                if elapsed < duration_ms:
                    progress = elapsed / duration_ms
                    current_height = start_height + (target_height - start_height) * progress
                    bar.set_height(current_height)
                    ax.figure.canvas.draw_idle()
                    comp_win.after(20, update_bar)
                else:
                    bar.set_height(target_height)
                    ax.figure.canvas.draw_idle()
            
            update_bar()

        # Plot LEFT graph with animation
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.set_ylabel("Time (seconds)", fontsize=12)
        ax1.set_title(f"{algo1} Execution Time", fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(time1, time2) * 1.2)
        ax1.ticklabel_format(style='plain', axis='y')
        
        bars1 = ax1.bar([algo1], [0], color=color1, width=0.5)
        bar1 = bars1[0]
        
        canvas1 = FigureCanvasTkAgg(fig1, master=left_graph_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Plot RIGHT graph with animation
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        ax2.set_ylabel("Time (seconds)", fontsize=12)
        ax2.set_title(f"{algo2} Execution Time", fontsize=14, fontweight='bold')
        ax2.set_ylim(0, max(time1, time2) * 1.2)
        ax2.ticklabel_format(style='plain', axis='y')
        
        bars2 = ax2.bar([algo2], [0], color=color2, width=0.5)
        bar2 = bars2[0]
        
        canvas2 = FigureCanvasTkAgg(fig2, master=right_graph_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

        # Start animations with delay
        def animate_both():
            # Add text labels to the bars
            def add_label_to_bar(ax, bar, time_val):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time_val:.6f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
                ax.figure.canvas.draw_idle()
            
            animate_bar(ax1, bar1, time1, f'{time1:.6f}s', 800)
            comp_win.after(400, lambda: animate_bar(ax2, bar2, time2, f'{time2:.6f}s', 800))
            comp_win.after(850, lambda: add_label_to_bar(ax1, bar1, time1))
            comp_win.after(1250, lambda: add_label_to_bar(ax2, bar2, time2))

        comp_win.after(200, animate_both)

        # Info frame at bottom
        info_frame = tk.Frame(comp_win)
        info_frame.pack(fill="x", padx=10, pady=10)

        # Determine winner
        if time1 < time2:
            winner = f"{algo1} is FASTER by {((time2-time1)/time2)*100:.2f}%"
            winner_color = "green"
        elif time2 < time1:
            winner = f"{algo2} is FASTER by {((time1-time2)/time1)*100:.2f}%"
            winner_color = "green"
        else:
            winner = "Both algorithms have equal performance"
            winner_color = "blue"

        info_label = tk.Label(info_frame,
            text=f"📊 {winner}",
            font=("Arial", 12, "bold"),
            fg=winner_color)
        info_label.pack(pady=5)

        # Stats frame
        stats_frame = tk.Frame(comp_win)
        stats_frame.pack(fill="x", padx=10, pady=5)

        stats_text = f"{algo1}: Comparisons={metrics1.comparisons}, Swaps={metrics1.swaps}  |  {algo2}: Comparisons={metrics2.comparisons}, Swaps={metrics2.swaps}"
        stats_label = tk.Label(stats_frame, text=stats_text, font=("Arial", 10))
        stats_label.pack()

        # Back button
        button_frame = tk.Frame(comp_win)
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"),
                  command=comp_win.destroy, width=20).pack()

# ---------------- Run ---------------- #

root = tk.Tk()
app = SortApp(root)
root.mainloop()