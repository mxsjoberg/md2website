# Glide Typing Problem in Python

*August 2023* [Python](programming.html#python) [Misc](programming.html#python-misc)

Glide typing is a feature on mobile devices that allows the user to type by swiping across the keyboard. The keyboard will predict the word based on the path of the swipe. The user can then select the word from the predicted list.

```python
input_ = "hgferyjkllkop"

words = ["coffee", "coding", "happy", "hello", "hop"]

chars = list(input_)

matches = []
for word in words:
    cidx = 0
    col = 0
    while col < len(chars):
        # print(chars[col], col)
        if chars[col] == word[cidx]:
            cidx += 1
            if cidx == len(word):
                matches.append((word, col))
                break
        col += 1

# all matches
print(matches)
# [('hello', 11), ('hop', 12)]

# first match
print(matches[0][0])
# hello
```