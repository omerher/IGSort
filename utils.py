import json
import requests
from datetime import datetime
import re


def get_id(username):
    url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=" + username + "&rank_token=0.3953592318270893&count=1"
    response = requests.get(url)
    respJSON = response.json()

    username_id = str(respJSON['users'][0].get("user").get("pk"))
    return username_id


def get_user_num_posts(account):
        r = requests.get("https://www.instagram.com/{}/?__a=1".format(account))
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

        ## check if the account has enough posts
        # user_posts = get_user_num_posts(account)
        # if num_posts > user_posts:
        #     num_posts = user_posts - 1

        max_id = ""
        while len(self.data) < num_posts:
            info = self.get_user_info(account_id, max_id)  # get targeted user's posts

            # parse through all posts
            try:
                posts = [post['node'] for post in info["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]
            except KeyError:
                return "An error has occurred. Please try again later."
            for post in posts:
                likes = post["edge_media_preview_like"]["count"]
                comments = post["edge_media_to_comment"]["count"]
                link = "https://instagram.com/p/{}/".format(post['shortcode'])
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
            
            if not info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]:  # check if more posts are available
                break
            
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
    r = requests.get("https://www.instagram.com/{}/?__a=1".format(account)).json()

    if r == {}:
        return {"error": True, "message": "User does not exist. Check for any spelling mistakes.", "code": 1}
    
    if isinstance(r, str):
        return {"error": True, "message": "Profile information could not be loaded at the current time. Top posts work as intented.", "code": 2}

    username = account
    full_name = r["graphql"]["user"]["full_name"]
    followers = r["graphql"]["user"]["edge_followed_by"]["count"]
    following = r["graphql"]["user"]["edge_follow"]["count"]
    bio = r["graphql"]["user"]["biography"]
    is_private = r["graphql"]["user"]["is_private"]
    is_verified = r["graphql"]["user"]["is_verified"]
    profile_picture = r["graphql"]["user"]["profile_pic_url_hd"]
    posts_count = r["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]

    account_info = {"error": False, "username": username, "full_name": full_name, "followers": followers, "following": following,
                    "bio": bio, "is_private": is_private, "is_verified": is_verified, "profile_picture": profile_picture,
                    "posts_count": posts_count}
    return account_info


def get_post_info(link):
    try:
        url = f"{link}?__a=1"
        json_data = requests.get(url).json()
    except:
        r = requests.get(link).text
        # find json in the html with regex, get first item from list then from tuple, and remove last semicolon
        x = re.findall('<script type="text\/javascript">' + '([^{]+?({.*graphql.*})[^}]+?)' + '<\/script>', r)[0][0][:-1]
        x = x.split('{"PostPage":[')[1].split(']},"hostname"')[0]  # cut JS text at the beginning and at the end
        json_data = json.loads(x)

    return json_data


def get_post_media(link):
    info = get_post_info(link)

    response = []
    
    # handle different paths for different media type
    if info["graphql"]["shortcode_media"]["__typename"] == "GraphImage":
        media = info["graphql"]["shortcode_media"]["display_url"]
        suffix = ".jpg"
        response.append({'media': media, 'suffix': suffix})
    elif info["graphql"]["shortcode_media"]["__typename"] == "GraphVideo":
        media = info["graphql"]["shortcode_media"]["video_url"]
        suffix = ".mp4"
        response.append({'media': media, 'suffix': suffix})
    elif info["graphql"]["shortcode_media"]["__typename"] == "GraphSidecar":
        for content in info["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]:
            if content["node"]["__typename"] == "GraphImage":
                media = content["node"]["display_url"]
                suffix = ".jpg"
                response.append({'media': media, 'suffix': suffix})
            elif content["node"]["__typename"] == "GraphVideo":
                media = (content["node"]["video_url"])
                suffix = ".mp4"
                response.append({'media': media, 'suffix': suffix})
    else:
        response = []

    return response