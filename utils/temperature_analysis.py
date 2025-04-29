
def first_order_difference(arr: list) -> bool:
    positive_steps = 0
    for i in range(len(arr) - 1):
        if arr[i+1] - arr[i] > 0:
            positive_steps += 1
    pos_ratio = positive_steps / (len(arr) - 1)
    return pos_ratio >= 0.6

# print(first_order_difference([11, 14, 15, 16, 20, 25]))