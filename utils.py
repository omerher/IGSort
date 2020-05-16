import json
import requests
from datetime import datetime


def get_id(username):
    url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=" + username + "&rank_token=0.3953592318270893&count=1"
    response = requests.get(url)
    respJSON = response.json()

    username_id = str(respJSON['users'][0].get("user").get("pk"))
    return username_id


def get_user_num_posts(account):
        r = requests.get(f"https://www.instagram.com/{account}/?__a=1")
        r_json = json.loads(r.text)
        return r_json["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
        # json.decoder.JSONDecodeError


def get_media_type(string):
    if string == "GraphImage":
        return "Photo"
    elif string == "GraphVideo":
        return "Video"
    elif string == "GraphSidecar":
        return "Carousel"


class InstagramScaper:
    def __init__(self):
        self.data = []

    def get_user_info(self, id, max_id):
        scrape_url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables={"id":' + id + ',"first":12,"after":"' + max_id + '"}'
        r = requests.get(scrape_url)

        return json.loads(r.text)

    def get_user_posts(self, account, num_posts):
        account_id = get_id(account)
        self.data = []

        # check if the account has enough posts

        # CURRENTLY NOT WORKING
        user_posts = get_user_num_posts(account)
        if num_posts > user_posts:
            num_posts = user_posts - 1

        max_id = ""
        while len(self.data) < num_posts:
            info = self.get_user_info(account_id, max_id)  # get targeted user's posts

            # parse through all posts
            posts = [post['node'] for post in info["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]
            for post in posts:
                likes = post["edge_media_preview_like"]["count"]
                comments = post["edge_media_to_comment"]["count"]
                link = f"https://instagram.com/p/{post['shortcode']}/"
                media_type = get_media_type(post["__typename"])
                try:
                    caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
                except IndexError:
                    caption = ""
                thumbnail = post["display_url"]
                published_date = datetime.utcfromtimestamp(post["taken_at_timestamp"]).strftime('%d %b, %Y %I:%M %p')  # formats time to string %d %b %Y - %H:%M UTC
                # gets view of post if it is a video
                if media_type == "Video":
                    views = post["video_view_count"]
                else:
                    views = None

                post_dict = {
                    "thumbnail": thumbnail,
                    "link": link,
                    "likes": likes,
                    "comments": comments,
                    "media_type": media_type,
                    "caption": caption,
                    "published_date": published_date,
                    "views": views
                }
                self.data.append(post_dict)

            max_id = info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]  # get max id for next batch

        self.data = self.data[:num_posts]  # removes last posts to match number of posts requested
        self.sort_posts()

    def sort_posts(self):
        # reverse = True (Sorts in descending order)
        # key is set to sort using second element of
        # sublist lambda has been used
        sub_li = self.data
        sub_li.sort(key=lambda x: int(x["likes"]), reverse=True)
        self.data = sub_li


def scrape(acc, num_posts):
    scraper = InstagramScaper()
    scraper.get_user_posts(acc, num_posts)
    return scraper.data

def get_user_info(account):
    r = requests.get(f"https://www.instagram.com/{account}/?__a=1").json()

    username = account
    full_name = r["graphql"]["user"]["full_name"]
    followers = r["graphql"]["user"]["edge_followed_by"]["count"]
    following = r["graphql"]["user"]["edge_follow"]["count"]
    bio = r["graphql"]["user"]["biography"]
    is_private = r["graphql"]["user"]["is_private"]
    is_verified = r["graphql"]["user"]["is_verified"]
    profile_picture = r["graphql"]["user"]["profile_pic_url_hd"]
    posts_count = r["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]

    account_info = {"username": username, "full_name": full_name, "followers": followers, "following": following,
                    "bio": bio, "is_private": is_private, "is_verified": is_verified, "profile_picture": profile_picture,
                    "posts_count": posts_count}
    return account_info
