import binary_tree as bt
import numpy as np
import string
import time

def main():
    """
    Test/validation of classes contained in binary_tree.py
    Set test flat value to run specific test:
        0: print tests
        1: find element test
        2: find element speed test
        other: properties (node count, height) and methods (find nearest, find kth)
    :return:
    """
    test_flag = -1

    # Find speed test quantity
    test_qty = 2 ** 10
    test_sze = 2 ** 12

    # Generate a tree
    n = 2 ** 4
    s = 116
    k = int(n / 2)
    seed = 1  # np.random.randint(low=0, high=2 ** 10, size=1)
    np.random.seed(seed)

    keys = np.random.randint(low=0, high=10 * n, size=n)

    t = bt.BT_Tree()
    for this_key in keys:
        random_letter = string.ascii_letters[np.random.randint(low=0, high=51, size=1)[0]]
        t.add(key=this_key, value=random_letter)

    # Run test
    if test_flag == 0:
        test_print(t, k)
    elif test_flag == 1:
        test_find_all(t, keys)
    elif test_flag == 2:
        del t
        del keys

        # Create a big tree
        t = bt.BT_Tree()
        keys = np.random.randint(low=0, high=10 * test_sze, size=test_sze)

        for this_key in keys:
            t.add(key=this_key)

        test_find_speed(tree=t, test_qty=test_qty, keys=keys)
    else:
        test_methods(tree=t, keys=keys, n=n, k=k, s=s)


def test_print(tree:bt.BT_Tree=None, k:int=0) -> None:
    print(16 * '=')
    print(f"Full tree")
    tree.print(print_key=True, print_val=True, max_print_height=-1)

    print(16 * '=')
    print(f"Branch from {k}th node")
    tree.print_branch(tree.find_kth(k), print_key=True, print_val=True)

def test_methods(tree:bt.BT_Tree=None, keys:np.ndarray=None, n:int=0, k:int=0, s:int=0) -> None:
    nearest_s = keys[np.argmin(np.abs(keys - s))]

    print(16 * '=')
    print(f"actual node count: {n}")
    print(f"node count property: {tree.node_count}")

    print(16 * '=')
    print(f"min height: {int(np.ceil(np.log2(n)))}")
    print(f"actual height: {tree.height}")

    print(16 * '=')
    print(f"nearest s = {s}: {nearest_s}")
    print(f"found nearest s = {s}: {tree.find_node(s, nearest=True).key}")

    print(16 * '=')
    print(f"{k}th element found by Numpy: {np.partition(keys, kth=k)[k]}")
    print(f"{k}th element found by BTree: {tree.find_kth(k).key}")

def test_find_all(tree:bt.BT_Tree=None, keys:np.ndarray=None):
    print(16 * '=')
    print("Find every node")
    sorted_keys = np.sort(keys)
    error_flag = False
    for idx, key in enumerate(keys):
        found_key = tree.find_kth(idx).key

        if sorted_keys[idx] != found_key:
            error_flag = False

        print(f"{idx:3}th is {sorted_keys[idx] == found_key}: {sorted_keys[idx]:3} == {found_key:3}")

    if error_flag:
        print("Mismatch between numpy.sort(keys)[kth] and bt.find(kth)")
    else:
        print("No mismatches between numpy.sort(keys)[kth] and bt.find(kth)")

def test_find_speed(tree:bt.BT_Tree=None, test_qty:int=0, keys:np.ndarray=None):
    # print(f"{k}th element found by Numpy: {np.partition(keys, kth=k)[k]}")

    k = int(keys.shape[0] / 2)

    t_tot_bt = 0.0
    for _ in range(test_qty):
        t_ini = time.perf_counter()
        tree.find_kth(k)
        t_tot_bt += (time.perf_counter() - t_ini)

    t_tot_np = 0.0
    for _ in range(test_qty):
        t_ini = time.perf_counter()
        np.partition(keys, k)
        t_tot_np += (time.perf_counter() - t_ini)


    print(f"average run time to find {k}th element among {keys.shape[0]} elements over {test_qty} trials:\n")
    print(f"Numpy partition     : {t_tot_np / test_qty:11.9f}  [s]")
    print(f"Binary Tree Search  : {t_tot_bt / test_qty:11.9f}  [s]")
    pass


if __name__ == '__main__':
    main()