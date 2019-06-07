from typing import List

# https://leetcode.com/problems/reverse-nodes-in-k-group/

## Reverse Nodes in k-Group - constant memory approach

class ListNode:
    """
    Node in singly linked list.
    """
    def __init__(self, x):
        self.val = x
        self.next = None

def listFromArray(array: List[int]) -> ListNode:
    """
    Make a linked list from an array. Return the head of the
    array. Return the head of the list.
    """
    head = ListNode(array[0])
    node = head
    for val in array[1:]:
        node.next = ListNode(val)
        node = node.next
    return head


def arrayOfListNodes(head: ListNode, k: int) -> List[ListNode]:
    """
    Make array of linked list nodes of max length k.
    """
    L = []
    node = head
    n = 1
    while node and n <= k:
        L += [node]
        node = node.next
        n += 1
    return L

def printNodes(head: ListNode) -> None:
    """
    Print nodes in linked list.
    """
    node = head
    while node:
        print(node.val)
        node = node.next

def reverseKGroup(head: ListNode, k: int) -> ListNode:
    """
    Given a linked list, reverse the nodes of a linked list
    k at a time and return its modified list.
    """
    # Degenerate case - no head passed
    if not head:
        return []
    if k == 1:
        return head
    node = head
    Lprev = None
    nextnode = node
    while nextnode:
        L = arrayOfListNodes(node, k)
        Lswap = []
        # At least k more nodes left.
        if len(L) == k:
            Li = []
            prev = L[0]
            Li = [prev] + Li
            for j in range(1, k):
                node = L[j]
                nextnode = node.next
                node.next = prev
                Li = [node] + Li
                prev = node
            Lswap += Li
        # Less than k nodes left; add to list
        else:
            Lswap += L
            nextnode = None
        if Lprev:
            tail1 = Lprev[-1]
            head2 = Lswap[0]
            tail1.next = head2
        else:
            head = Lswap[0]
        Lprev = Lswap
        node = nextnode
    # Make last node next field null
    Lswap[-1].next = None
    return head

class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        return reverseKGroup(head, k)        
