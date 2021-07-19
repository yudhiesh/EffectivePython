import requests, time


"""
This is slow because for each request it waits for the current request to finish
before making the next request. 
If a single requests takes 1 second then 10 would take 10 seconds
"""

words = ["hello", "mellow", "cat", "rat", "dog", "frog", "mouse", "sparrow", "man", "women"]

def make_req_syncronously(words_arr):
    final_res = []
    for word in words_arr:
        url = f"https://api.datamuse.com/words?rel_rhy={word}&max=100"
        response = requests.get(url)
        json_response = response.json()
        for item in json_response:
            rhyming_word = item.get("word", "")
            final_res.append({"word": word, "rhyming_word": rhyming_word})
    return final_res

without_async_start_time = time.time()
response = make_req_syncronously(words)
time_without_async = time.time() - without_async_start_time

print("total time for with synchronous execution >> ", time_without_async, " seconds")

