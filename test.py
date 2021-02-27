import time

def test_send(request, receive):
    while True:
        next_task = request.get()
        time.sleep(1)
        print("test data: " + next_task[0] + next_task[1])
        receive.put("test data: " + next_task[0] + next_task[1])
    return
