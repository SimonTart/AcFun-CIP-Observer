import arrow

def formatTimestamp(timestamp):
    # timestamp交给arrow食用需要去除 1000
    return arrow.get(timestamp / 1000).to('GMT+8').format('YYYY-MM-DD HH:mm:ss')