import asyncio
import aiohttp  # external library
import time

words = [
    "hello",
    "mellow",
    "cat",
    "rat",
    "dog",
    "frog",
    "mouse",
    "sparrow",
    "man",
    "women",
]


def merge_lists(results_from_fc):
    """
    Function for merging multiple lists
    """
    combined_list = []
    for li in results_from_fc:
        combined_list.extend(li)
    return combined_list


async def main():
    headers = {"content-type": "application/json"}
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []  # for storing all the tasks we will create in the next step
        for word in words:
            task = asyncio.ensure_future(
                get_rhyming_words(session, word)
            )  # means get this process started and move on
            tasks.append(task)

        # .gather() will collect the result from every single task from tasks list
        # here we use await to wait till all the requests have been satisfied
        all_results = await asyncio.gather(*tasks)
        combined_list = merge_lists(all_results)
        return combined_list


async def get_rhyming_words(session, word):
    url = f"https://api.datamuse.com/words?rel_rhy={word}&max=1000"
    async with session.get(url) as response:
        result_data = await response.json()
        return result_data


async_func_start_time = time.time()
response2 = asyncio.get_event_loop().run_until_complete(main(words))
time_with_async = time.time() - async_func_start_time

print("\nTotal time with async/await execution >> ", time_with_async, " seconds")
