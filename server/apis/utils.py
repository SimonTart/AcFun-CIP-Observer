import re

def processEmotion(comment):
    emotionImage = r'<img class="emotion" src="http://cdn.aixifan.com/dotnet/20130418/umeditor/dialogs/emotion/images/\g<name>/\g<number>.gif" />'
    emotionRe = re.compile(r'\[emot=(?P<name>\w+),(?P<number>\d+)\/]')

    image = r'<img src="\g<url>" />'
    imageRe =  re.compile(r'\[img=图片\](?P<url>[\w\d:\/.]+)\[/img\]')

    comment = emotionRe.sub(emotionImage, comment)
    comment = imageRe.sub(image, comment)

    return comment