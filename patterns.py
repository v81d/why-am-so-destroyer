import re

PATTERNS = [
    re.compile(r"(why|🇼[\W]*🇭[\W]*🇾|🇼[\W]*h[\W]*y|w[\W]*🇭[\W]*🇾|[\W]*w[\W]*h[\W]*y|whу|🇼[\W]*🇭[\W]*у|🇼[\W]*h[\W]*у|w[\W]*🇭[\W]*у|[\W]*w[\W]*h[\W]*у|шну|🇼[\W]*🇭[\W]*🇾|🇼[\W]*h[\W]*у|w[\W]*🇭[\W]*у|[\W]*ш[\W]*н[\W]*у)", re.IGNORECASE), # 1
    re.compile(r"🇾[\W_a-zа-я]*🇲[\W_a-zа-я]*🇸[🇴0о]", re.IGNORECASE), # 2
    re.compile(r"y[\W_🇦-🇿а-я]*m[\W_🇦-🇿а-я]*s[o0о]", re.IGNORECASE), # 3
    re.compile(r"(why|w[\W]*h[\W]*y|🇼[\W]*🇭[\W]*🇾|[\W]*w[\W]*h[\W]*y|whу|🇼[\W]*🇭[\W]*у|🇼[\W]*h[\W]*у|w[\W]*🇭[\W]*у|[\W]*w[\W]*h[\W]*у|шну|🇼[\W]*🇭[\W]*🇾|🇼[\W]*h[\W]*у|w[\W]*🇭[\W]*у|[\W]*ш[\W]*н[\W]*у)[\W]*(am|🇦[\W]*🇲|a[\W]*m|m|🇦[\W]*🇲|a[\W]*m|аm|🇦[\W]*🇲|а[\W]*m)[\W]*(so|🇸[\W]*🇴|s[\W]*o|s[\W]*0|🇸[\W]*🇴|s[\W]*о|s[\W]*0|sо|🇸[\W]*🇴|s[\W]*о|s[\W]*0)", re.IGNORECASE), # 4
    re.compile(r"(y|🇾|у)[\W]*(m|🇲|am|🇦[\W]*🇲|a[\W]*m|m|🇦[\W]*🇲|a[\W]*m|аm|🇦[\W]*🇲|а[\W]*m)[\W]*(so|🇸[\W]*🇴|s[\W]*o|s[\W]*0|🇸[\W]*🇴|s[\W]*о|s[\W]*0|sо|🇸[\W]*🇴|s[\W]*о|s[\W]*0)", re.IGNORECASE) # 5
]  # Feel free to add more RegEx patterns here