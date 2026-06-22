import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def fetch_posts(user_id):
    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"User {user_id} - Request failed" )
        return []

def count_posts(all_posts):
    result = {}

    for user_posts in all_posts:
        if user_posts:
            user_id = user_posts[0]["userId"]
            result[user_id] = len(user_posts)

    return result

def find_longest_post(all_posts):
    longest = None
    for user_posts in all_posts:
        for post in user_posts:
            if longest is None or len(post["body"]) > len(longest["body"] ):
                longest = post

    return {
        "userId": longest["userId"],
        "title": longest["title"],
        "length": len(longest["body"])
    }

def average_title_length(all_posts):
    titles = []
    for user_posts in all_posts:
        for post in user_posts:
            titles.append(len(post["title"]))

    return sum(titles) / len(titles)

if __name__ == "__main__":
    user_ids = [1, 2, 3, 4, 5]
    with ThreadPoolExecutor(max_workers=5) as executor:
        all_posts = list(executor.map(fetch_posts, user_ids) )
    with ProcessPoolExecutor() as executor:
        future1 = executor.submit(count_posts, all_posts)
        future2 = executor.submit(find_longest_post, all_posts)
        future3 = executor.submit(average_title_length, all_posts)

        posts_count = future1.result()
        longest_post = future2.result()
        avg_title = future3.result()

    print("\n" + "=" * 60)
    print("                 POST ANALYSIS REPORT")
    print("=" * 60)

    print("\nPOST COUNT BY USER")
    print("-" * 60)

    for user, count in posts_count.items():
        print(f"User {user:<5} | {count} posts")

    print("\n" + "-" * 60)
    print("LONGEST POST")
    print("-" * 60)
    print(f"User ID       : {longest_post['userId']}")
    print(f"Title         : {longest_post['title']}")
    print(f"Body Length   : {longest_post['length']} characters")

    print("\n" + "-" * 60)
    print("GENERAL STATISTICS")
    print("-" * 60)
    print(f"Average title length: {avg_title:.2f} characters")

    print("\n" + "=" * 60)
    print("End of report")
    print("=" * 60)
