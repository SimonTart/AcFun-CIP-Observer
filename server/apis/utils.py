import re

def processEmotion(comment):
    image = r'<img class="emotion" src="http://cdn.aixifan.com/dotnet/20130418/umeditor/dialogs/emotion/images/\g<name>/\g<number>.gif" />'
    emotionRe = re.compile(r'\[emot=(?P<name>\w+),(?P<number>\d+)\/]')
    return emotionRe.sub(image, comment)