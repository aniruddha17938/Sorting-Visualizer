from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Sorting Algorithms with Step Tracking
def bubble_sort(arr):
    steps = []
    arr_copy = arr[:]
    for i in range(len(arr_copy)):
        for j in range(len(arr_copy) - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                steps.append(arr_copy[:])
    return steps

def insertion_sort(arr):
    steps = []
    arr_copy = arr[:]
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        while j >= 0 and arr_copy[j] > key:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
            steps.append(arr_copy[:])  # Capture step
        arr_copy[j + 1] = key
        steps.append(arr_copy[:])
    return steps

def merge_sort(arr):
    steps = []
    arr_copy = arr[:]
    
    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)
    
    def merge(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] < right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
            steps.append(arr[:])  # Capture step
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            steps.append(arr[:])
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            steps.append(arr[:])

    merge_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return steps

def quick_sort(arr):
    steps = []
    arr_copy = arr[:]

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr[:])  # Capture step
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr[:])  # Capture step
        return i + 1

    quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return steps

# API Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sort', methods=['POST'])
def sort():
    data = request.json
    array = data.get("array", [])
    algorithm = data.get("algorithm", "bubble_sort")

    if not array:
        return jsonify({"error": "Invalid input"}), 400

    sorting_algorithms = {
        "bubble_sort": bubble_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort,
    }

    if algorithm not in sorting_algorithms:
        return jsonify({"error": "Invalid sorting algorithm"}), 400

    steps = sorting_algorithms[algorithm](array)
    return jsonify({"steps": steps})

if __name__ == '__main__':
    app.run(debug=True)