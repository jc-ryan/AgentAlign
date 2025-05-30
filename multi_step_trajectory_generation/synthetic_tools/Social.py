"""
Social media platform simulation functions.
This module provides mock implementations of posting and commenting functionalities
for various social media platforms including Twitter/X, Instagram, Weibo, TikTok,
YouTube, and Bilibili.
"""

import time
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Union, Any

# Common utility functions
def generate_id(prefix: str = "") -> str:
    """Generates a unique ID with optional prefix."""
    return f"{prefix}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# Twitter/X Functions
def get_twitter_profile(
    user_id: str,
    include_pinned_tweet: bool = False,
    include_metrics: bool = True
) -> Dict[str, Any]:
    """Get Twitter/X user profile information."""
    if not user_id:
        return {"error": "User ID is required"}
        
    response = {
        "id": f"user_{user_id}" if not user_id.startswith("user_") else user_id,
        "username": user_id.lower().replace(" ", "_"),
        "name": f"User {user_id}",
        "bio": f"This is a mock bio for {user_id}",
        "profile_image_url": f"https://example.com/avatars/{user_id}.jpg",
        "created_at": "2020-01-01T00:00:00Z",
        "verified": random.choice([True, False]),
        "verified_type": random.choice([None, "blue", "government", "business"]),
        "location": "San Francisco, CA",
        "url": f"https://example.com/{user_id}",
    }
    
    if include_metrics:
        response["public_metrics"] = {
            "followers_count": random.randint(100, 10000),
            "following_count": random.randint(50, 1000),
            "tweet_count": random.randint(100, 5000),
            "listed_count": random.randint(0, 100)
        }
        
    if include_pinned_tweet:
        response["pinned_tweet_id"] = f"tw_{random.randint(1000, 9999)}"
        
    return response

def search_twitter_content(
    query: str,
    search_type: str = "mixed",
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
    next_token: Optional[str] = None
) -> Dict[str, Any]:
    """Search Twitter/X content (tweets, users, or both)."""
    if not query:
        return {"error": "Search query is required"}
        
    if filters is None:
        filters = {}
        
    results = {
        "data": [],
        "meta": {
            "result_count": 0,
            "next_token": f"next_{random.randint(1000, 9999)}",
            "query": query
        }
    }
    
    for i in range(min(limit, 20)):
        if search_type in ["users", "mixed"]:
            user = {
                "id": f"user_{random.randint(1000, 9999)}",
                "username": f"user_{i}_{query.replace(' ', '_')}",
                "name": f"User {i}",
                "description": f"Profile matching query: {query}",
                "profile_image_url": f"https://example.com/avatars/user_{i}.jpg",
                "verified": random.choice([True, False]),
                "metrics": {
                    "followers_count": random.randint(100, 10000),
                    "following_count": random.randint(50, 1000),
                    "tweet_count": random.randint(100, 5000)
                }
            }
            results["data"].append({"type": "user", "data": user})
            
        if search_type in ["tweets", "mixed"]:
            tweet = {
                "id": f"tw_{random.randint(1000, 9999)}",
                "text": f"Tweet {i} matching query: {query}",
                "created_at": get_current_timestamp(),
                "author_id": f"user_{random.randint(1000, 9999)}",
                "metrics": {
                    "retweet_count": random.randint(0, 1000),
                    "reply_count": random.randint(0, 500),
                    "like_count": random.randint(0, 2000),
                    "quote_count": random.randint(0, 100)
                },
                "lang": filters.get("language", "en")
            }
            results["data"].append({"type": "tweet", "data": tweet})
    
    results["meta"]["result_count"] = len(results["data"])
    return results

# Instagram Functions
def get_instagram_profile(
    user_id: str,
    include_stories: bool = False,
    include_business_metrics: bool = False
) -> Dict[str, Any]:
    """Get Instagram user profile information."""
    if not user_id:
        return {"error": "User ID is required"}
        
    response = {
        "id": f"ig_{user_id}" if not user_id.startswith("ig_") else user_id,
        "username": user_id.lower().replace(" ", "_"),
        "full_name": f"User {user_id}",
        "biography": f"This is a mock bio for {user_id}",
        "profile_picture_url": f"https://example.com/ig_avatars/{user_id}.jpg",
        "is_private": random.choice([True, False]),
        "is_verified": random.choice([True, False]),
        "external_url": f"https://example.com/{user_id}",
        "media_count": random.randint(10, 1000),
        "follower_count": random.randint(100, 1000000),
        "following_count": random.randint(100, 1000),
        "category": random.choice(["Creator", "Athlete", "Artist", None])
    }
    
    if include_stories:
        response["stories"] = {
            "count": random.randint(0, 20),
            "highlights": [
                {
                    "id": f"highlight_{i}",
                    "title": f"Highlight {i}",
                    "cover_url": f"https://example.com/highlights/{i}.jpg",
                    "media_count": random.randint(1, 100)
                } for i in range(random.randint(0, 5))
            ]
        }
        
    if include_business_metrics:
        response["business_metrics"] = {
            "website_clicks": random.randint(0, 10000),
            "email_contacts": random.randint(0, 1000),
            "get_directions_clicks": random.randint(0, 500),
            "impression_count": random.randint(1000, 100000),
            "reach": random.randint(500, 50000),
            "profile_views": random.randint(100, 10000)
        }
        
    return response

def search_instagram_content(
    query: str,
    search_type: str = "top",  # top, users, tags, places
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
    next_token: Optional[str] = None
) -> Dict[str, Any]:
    """Search Instagram content."""
    if not query:
        return {"error": "Search query is required"}
        
    if filters is None:
        filters = {}
        
    results = {
        "data": [],
        "paging": {
            "next_token": f"ig_next_{random.randint(1000, 9999)}",
            "total_count": random.randint(limit, 1000)
        }
    }
    
    for i in range(min(limit, 20)):
        if search_type in ["users", "top"]:
            user = {
                "id": f"ig_user_{random.randint(1000, 9999)}",
                "username": f"ig_user_{i}_{query.replace(' ', '_')}",
                "full_name": f"Instagram User {i}",
                "profile_picture_url": f"https://example.com/ig_avatars/user_{i}.jpg",
                "is_verified": random.choice([True, False]),
                "follower_count": random.randint(100, 1000000),
                "media_count": random.randint(1, 1000),
                "category": random.choice(["Creator", "Athlete", "Artist", None])
            }
            results["data"].append({"type": "user", "data": user})
            
        if search_type in ["tags", "top"]:
            hashtag = {
                "id": f"tag_{random.randint(1000, 9999)}",
                "name": f"{query.replace(' ', '')}_{i}",
                "media_count": random.randint(1, 1000000),
                "trending_score": random.randint(1, 100)
            }
            results["data"].append({"type": "hashtag", "data": hashtag})
            
        if search_type in ["places", "top"]:
            place = {
                "id": f"place_{random.randint(1000, 9999)}",
                "name": f"Place {i} near {query}",
                "address": f"123 {query} St",
                "city": "Sample City",
                "media_count": random.randint(1, 10000),
                "lat": random.uniform(-90, 90),
                "lng": random.uniform(-180, 180)
            }
            results["data"].append({"type": "place", "data": place})
    
    return results

# TikTok Functions
def get_tiktok_profile(
    user_id: str,
    include_live_status: bool = False,
    include_commerce_info: bool = False
) -> Dict[str, Any]:
    """Get TikTok user profile information."""
    if not user_id:
        return {"error": "User ID is required"}
        
    response = {
        "id": f"tt_{user_id}" if not user_id.startswith("tt_") else user_id,
        "unique_id": user_id.lower().replace(" ", "_"),
        "nickname": f"TikTok User {user_id}",
        "avatar_url": f"https://example.com/tt_avatars/{user_id}.jpg",
        "bio": f"This is a mock TikTok bio for {user_id}",
        "verified": random.choice([True, False]),
        "creator_level": random.randint(1, 5),
        "stats": {
            "following_count": random.randint(0, 1000),
            "follower_count": random.randint(100, 1000000),
            "like_count": random.randint(1000, 10000000),
            "video_count": random.randint(1, 1000)
        }
    }
    
    if include_live_status:
        response["live_status"] = {
            "is_live": random.choice([True, False]),
            "current_viewers": random.randint(0, 10000),
            "total_viewers": random.randint(0, 100000),
            "gifts_received": random.randint(0, 1000)
        }
        
    if include_commerce_info:
        response["commerce_info"] = {
            "shop_enabled": random.choice([True, False]),
            "shop_name": f"Shop {user_id}",
            "product_count": random.randint(0, 100),
            "shop_url": f"https://example.com/tt_shop/{user_id}"
        }
        
    return response

def search_tiktok_content(
    query: str,
    search_type: str = "general",  # general, user, video, music, hashtag
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
    cursor: Optional[str] = None
) -> Dict[str, Any]:
    """Search TikTok content."""
    if not query:
        return {"error": "Search query is required"}
        
    if filters is None:
        filters = {}
        
    results = {
        "data": [],
        "cursor": str(random.randint(1000, 9999)),
        "has_more": random.choice([True, False])
    }
    
    for i in range(min(limit, 20)):
        if search_type in ["user", "general"]:
            user = {
                "id": f"tt_user_{random.randint(1000, 9999)}",
                "unique_id": f"user_{i}_{query.replace(' ', '_')}",
                "nickname": f"TikTok User {i}",
                "avatar_url": f"https://example.com/tt_avatars/user_{i}.jpg",
                "verified": random.choice([True, False]),
                "follower_count": random.randint(100, 1000000),
                "like_count": random.randint(1000, 10000000)
            }
            results["data"].append({"type": "user", "data": user})
            
        if search_type in ["video", "general"]:
            video = {
                "id": f"video_{random.randint(1000, 9999)}",
                "desc": f"Video {i} matching {query}",
                "create_time": get_current_timestamp(),
                "author": f"tt_user_{random.randint(1000, 9999)}",
                "stats": {
                    "play_count": random.randint(1000, 1000000),
                    "like_count": random.randint(100, 100000),
                    "comment_count": random.randint(10, 10000),
                    "share_count": random.randint(1, 1000)
                }
            }
            results["data"].append({"type": "video", "data": video})
            
        if search_type in ["music", "general"]:
            music = {
                "id": f"music_{random.randint(1000, 9999)}",
                "title": f"Music {i} matching {query}",
                "author": f"Artist {i}",
                "duration": random.randint(15, 60),
                "album": f"Album {i}",
                "play_count": random.randint(1000, 1000000)
            }
            results["data"].append({"type": "music", "data": music})
    
    return results

def search_youtube_content(
    query: str,
    search_type: str = "mixed",  # video, channel, playlist, mixed
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """Search YouTube content."""
    if not query:
        return {"error": "Search query is required"}
        
    if filters is None:
        filters = {}
        
    results = {
        "items": [],
        "page_info": {
            "total_results": random.randint(limit, 10000),
            "results_per_page": min(limit, 20),
            "next_page_token": f"yt_next_{random.randint(1000, 9999)}",
        },
        "region_code": filters.get("region", "US")
    }
    
    for i in range(min(limit, 20)):
        if search_type in ["channel", "mixed"]:
            channel = {
                "id": f"yt_channel_{random.randint(1000, 9999)}",
                "type": "channel",
                "snippet": {
                    "title": f"Channel {i} matching {query}",
                    "description": f"YouTube channel related to {query}",
                    "custom_url": f"@{query.replace(' ', '')}_{i}",
                    "thumbnail_url": f"https://example.com/yt_channels/{i}.jpg",
                    "country": "US"
                },
                "statistics": {
                    "subscriber_count": random.randint(100, 1000000),
                    "video_count": random.randint(1, 1000),
                    "view_count": random.randint(1000, 10000000)
                }
            }
            results["items"].append(channel)
            
        if search_type in ["video", "mixed"]:
            video = {
                "id": f"yt_video_{random.randint(1000, 9999)}",
                "type": "video",
                "snippet": {
                    "title": f"Video {i} matching {query}",
                    "description": f"YouTube video about {query}",
                    "channel_id": f"channel_{random.randint(1000, 9999)}",
                    "published_at": get_current_timestamp(),
                    "thumbnails": {
                        "default": f"https://example.com/yt_videos/{i}_default.jpg",
                        "high": f"https://example.com/yt_videos/{i}_high.jpg"
                    }
                },
                "statistics": {
                    "view_count": random.randint(100, 1000000),
                    "like_count": random.randint(10, 100000),
                    "comment_count": random.randint(0, 10000)
                },
                "content_details": {
                    "duration": f"PT{random.randint(1, 60)}M{random.randint(0, 59)}S",
                    "definition": random.choice(["hd", "sd"])
                }
            }
            results["items"].append(video)
            
        if search_type in ["playlist", "mixed"]:
            playlist = {
                "id": f"yt_playlist_{random.randint(1000, 9999)}",
                "type": "playlist",
                "snippet": {
                    "title": f"Playlist {i} matching {query}",
                    "description": f"Collection of videos about {query}",
                    "channel_id": f"channel_{random.randint(1000, 9999)}",
                    "thumbnail_url": f"https://example.com/yt_playlists/{i}.jpg"
                },
                "content_details": {
                    "item_count": random.randint(1, 100)
                }
            }
            results["items"].append(playlist)
    
    return results

# Bilibili Functions
def get_bilibili_profile(
    user_id: str,
    include_live: bool = False,
    include_bangumi: bool = False
) -> Dict[str, Any]:
    """Get Bilibili user profile information."""
    if not user_id:
        return {"error": "User ID is required"}
        
    response = {
        "mid": int(user_id) if str(user_id).isdigit() else random.randint(10000, 99999),
        "name": f"Bilibili用户 {user_id}",
        "sign": f"这是用户 {user_id} 的个性签名",
        "level": random.randint(0, 6),
        "coins": random.randint(0, 10000),
        "face": f"https://example.com/bili_avatars/{user_id}.jpg",
        "fans_badge": random.choice([True, False]),
        "official": {
            "role": random.randint(0, 3),  # 0: none, 1: personal, 2: org, 3: media
            "title": random.choice(["知名UP主", "机构认证", "官方认证", None]),
            "desc": "优质创作者"
        },
        "vip": {
            "type": random.randint(0, 2),  # 0: none, 1: monthly, 2: yearly
            "status": random.randint(0, 1),
            "due_date": (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        },
        "pendant": {
            "pid": random.randint(1, 1000),
            "name": "装饰挂件",
            "image": f"https://example.com/bili_pendants/{random.randint(1, 100)}.png"
        },
        "nameplate": {
            "nid": random.randint(1, 100),
            "name": "名片装饰",
            "image": f"https://example.com/bili_nameplates/{random.randint(1, 50)}.png"
        },
        "statistics": {
            "following": random.randint(0, 1000),
            "follower": random.randint(0, 1000000),
            "video_count": random.randint(0, 1000),
            "article_count": random.randint(0, 100),
            "likes": random.randint(0, 1000000)
        }
    }
    
    if include_live:
        response["live_info"] = {
            "live_status": random.randint(0, 1),  # 0: offline, 1: online
            "room_id": random.randint(10000, 99999),
            "room_title": "直播间标题",
            "room_cover": f"https://example.com/bili_rooms/{user_id}.jpg",
            "online_viewers": random.randint(0, 10000),
            "area_name": random.choice(["游戏", "知识", "娱乐", "电台"]),
        }
        
    if include_bangumi:
        response["bangumi_info"] = {
            "watching_count": random.randint(0, 50),
            "watched_count": random.randint(0, 200),
            "collection_count": random.randint(0, 500),
            "season_follows": [
                {
                    "season_id": random.randint(1000, 9999),
                    "title": f"番剧 {i}",
                    "progress": f"{random.randint(1, 12)}/{random.randint(12, 24)}",
                    "update_time": get_current_timestamp()
                } for i in range(random.randint(1, 5))
            ]
        }
        
    return response

def search_bilibili_content(
    query: str,
    search_type: str = "all",  # video, user, live, article, bangumi
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
    page: int = 1
) -> Dict[str, Any]:
    """Search Bilibili content."""
    if not query:
        return {"error": "Search query is required"}
        
    if filters is None:
        filters = {}
        
    results = {
        "page": page,
        "page_size": min(limit, 20),
        "total": random.randint(limit, 10000),
        "items": []
    }
    
    for i in range(min(limit, 20)):
        if search_type in ["user", "all"]:
            user = {
                "mid": random.randint(10000, 99999),
                "name": f"用户{i}_{query}",
                "face": f"https://example.com/bili_avatars/user_{i}.jpg",
                "level": random.randint(0, 6),
                "fans": random.randint(0, 1000000),
                "videos": random.randint(0, 1000),
                "sign": f"UP主简介 {query}",
                "official_verify": {
                    "type": random.randint(-1, 1),
                    "desc": random.choice(["知名UP主", "机构认证", None])
                }
            }
            results["items"].append({"type": "user", "data": user})
            
        if search_type in ["video", "all"]:
            video = {
                "aid": random.randint(10000, 99999),
                "bvid": f"BV{random.randint(10000, 99999)}",
                "title": f"视频{i}: {query}",
                "desc": f"视频描述 {query}",
                "pic": f"https://example.com/bili_videos/{i}.jpg",
                "owner": {
                    "mid": random.randint(10000, 99999),
                    "name": f"UP主{i}"
                },
                "stat": {
                    "view": random.randint(100, 1000000),
                    "danmaku": random.randint(10, 100000),
                    "reply": random.randint(0, 10000),
                    "favorite": random.randint(0, 50000),
                    "coin": random.randint(0, 10000),
                    "share": random.randint(0, 5000),
                    "like": random.randint(0, 100000)
                },
                "duration": random.randint(60, 3600),
                "pubdate": int(time.time()) - random.randint(0, 86400 * 30),
                "tname": random.choice(["知识", "游戏", "生活", "动画"])
            }
            results["items"].append({"type": "video", "data": video})
            
        if search_type in ["live", "all"]:
            live = {
                "roomid": random.randint(10000, 99999),
                "uid": random.randint(10000, 99999),
                "title": f"直播{i}: {query}",
                "uname": f"主播{i}",
                "online": random.randint(0, 10000),
                "cover": f"https://example.com/bili_lives/{i}.jpg",
                "area_name": random.choice(["游戏", "知识", "娱乐", "电台"]),
                "area_v2_name": "具体分区",
                "tags": [query, "直播", random.choice(["游戏", "知识", "娱乐"])],
                "live_status": random.randint(0, 1)
            }
            results["items"].append({"type": "live", "data": live})
            
        if search_type in ["article", "all"]:
            article = {
                "id": random.randint(10000, 99999),
                "title": f"专栏{i}: {query}",
                "summary": f"文章摘要 {query}",
                "banner_url": f"https://example.com/bili_articles/{i}.jpg",
                "author": {
                    "mid": random.randint(10000, 99999),
                    "name": f"作者{i}"
                },
                "stats": {
                    "view": random.randint(100, 10000),
                    "favorite": random.randint(0, 1000),
                    "like": random.randint(0, 2000),
                    "reply": random.randint(0, 500)
                },
                "publish_time": get_current_timestamp(),
                "category": random.choice(["生活", "游戏", "动画", "科技"])
            }
            results["items"].append({"type": "article", "data": article})
            
        if search_type in ["bangumi", "all"]:
            bangumi = {
                "season_id": random.randint(10000, 99999),
                "title": f"番剧{i}: {query}",
                "cover": f"https://example.com/bili_bangumis/{i}.jpg",
                "pub_time": get_current_timestamp(),
                "total_count": random.randint(1, 100),
                "newest_ep": {
                    "title": f"第{random.randint(1, 24)}话",
                    "pub_time": get_current_timestamp()
                }
            }
            results["items"].append({"type": "bangumi", "data": bangumi})
    
    return results

# Twitter/X Functions
def post_tweet(
    content: str,
    media_urls: Optional[List[str]] = None,
    reply_to_id: Optional[str] = None,
    is_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Simulates posting a tweet on Twitter/X platform.
    
    Args:
        content: Tweet text content (required)
        media_urls: List of media URLs (optional, max 4 images or 1 video)
        reply_to_id: ID of tweet being replied to (optional)
        is_sensitive: Flag for sensitive content (optional)
    
    Returns:
        Dict containing tweet details or error message
    """
    if not content and not media_urls:
        return {"error": "Tweet must contain either text or media"}
    if len(content) > 280:
        return {"error": "Tweet exceeds 280 characters"}
    if media_urls and len(media_urls) > 4:
        return {"error": "Maximum 4 media items allowed"}

    tweet_id = generate_id("tw")
    
    response = {
        "id": tweet_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "author_id": "user_12345",
        "metrics": {
            "likes": 0,
            "retweets": 0,
            "replies": 0,
            "views": 1
        },
        "lang": "en",
        "status": "posted"
    }

    if media_urls:
        response["media"] = [
            {
                "type": "photo" if url.endswith(('.jpg','.png','.jpeg')) else "video",
                "url": url,
                "status": "processed"
            } for url in media_urls
        ]
    if reply_to_id:
        response["in_reply_to_tweet_id"] = reply_to_id
    if is_sensitive:
        response["possibly_sensitive"] = True

    return response

def post_tweet_comment(
    tweet_id: str,
    content: str,
    media_urls: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on a tweet.
    """
    if not tweet_id:
        return {"error": "Tweet ID is required"}
    
    return post_tweet(content=content, media_urls=media_urls, reply_to_id=tweet_id)

# Instagram Functions
def post_instagram(
    media_urls: List[str],
    caption: Optional[str] = None,
    location: Optional[str] = None,
    user_tags: Optional[List[str]] = None,
    is_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Simulates posting content on Instagram.
    
    Args:
        media_urls: List of media URLs (required, max 10 images or 1 video)
        caption: Post caption (optional, max 2200 characters)
        location: Location tag (optional)
        user_tags: List of tagged users (optional)
        is_sensitive: Flag for sensitive content (optional)
    
    Returns:
        Dict containing post details or error message
    """
    if not media_urls:
        return {"error": "At least one media item is required"}
    if len(media_urls) > 10:
        return {"error": "Maximum 10 media items allowed"}
    if caption and len(caption) > 2200:
        return {"error": "Caption exceeds 2200 characters"}

    post_id = generate_id("ig")
    
    response = {
        "id": post_id,
        "created_at": get_current_timestamp(),
        "media": [
            {
                "type": "photo" if url.endswith(('.jpg','.png','.jpeg')) else "video",
                "url": url,
                "status": "processed"
            } for url in media_urls
        ],
        "metrics": {
            "likes": 0,
            "comments": 0,
            "saves": 0,
            "shares": 0
        },
        "status": "posted"
    }

    if caption:
        response["caption"] = caption
    if location:
        response["location"] = {"name": location}
    if user_tags:
        response["user_tags"] = user_tags
    if is_sensitive:
        response["sensitivity_flag"] = True

    return response

def post_instagram_comment(
    post_id: str,
    content: str,
    reply_to_comment_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on an Instagram post.
    """
    if not post_id:
        return {"error": "Post ID is required"}
    if not content:
        return {"error": "Comment content is required"}
    if len(content) > 2200:
        return {"error": "Comment exceeds 2200 characters"}

    comment_id = generate_id("igc")
    
    response = {
        "id": comment_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "post_id": post_id,
        "metrics": {
            "likes": 0,
            "replies": 0
        },
        "status": "posted"
    }

    if reply_to_comment_id:
        response["in_reply_to_comment_id"] = reply_to_comment_id

    return response

# Weibo Functions
def post_weibo(
    content: str,
    media_urls: Optional[List[str]] = None,
    topics: Optional[List[str]] = None,
    location: Optional[str] = None,
    is_sensitive: bool = False,
    visible_to: str = "public"
) -> Dict[str, Any]:
    """
    Simulates posting content on Weibo.
    
    Args:
        content: Post text content (required, max 2000 characters)
        media_urls: List of media URLs (optional, max 9 images or 1 video)
        topics: List of hashtag topics (optional)
        location: Location tag (optional)
        is_sensitive: Flag for sensitive content (optional)
        visible_to: Visibility setting (optional, default "public")
    
    Returns:
        Dict containing post details or error message
    """
    if not content:
        return {"error": "Content is required"}
    if len(content) > 2000:
        return {"error": "Content exceeds 2000 characters"}
    if media_urls and len(media_urls) > 9:
        return {"error": "Maximum 9 media items allowed"}

    post_id = generate_id("wb")
    
    response = {
        "id": post_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "metrics": {
            "likes": 0,
            "reposts": 0,
            "comments": 0,
            "reads": 1
        },
        "visibility": visible_to,
        "status": "posted"
    }

    if media_urls:
        response["media"] = [
            {
                "type": "photo" if url.endswith(('.jpg','.png','.jpeg')) else "video",
                "url": url,
                "status": "processed"
            } for url in media_urls
        ]
    if topics:
        response["topics"] = topics
    if location:
        response["location"] = {"name": location}
    if is_sensitive:
        response["sensitivity_flag"] = True

    return response

def post_weibo_comment(
    post_id: str,
    content: str,
    media_urls: Optional[List[str]] = None,
    reply_to_comment_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on a Weibo post.
    """
    if not post_id:
        return {"error": "Post ID is required"}
    if not content:
        return {"error": "Comment content is required"}
    if len(content) > 1000:
        return {"error": "Comment exceeds 1000 characters"}
    if media_urls and len(media_urls) > 9:
        return {"error": "Maximum 9 media items allowed"}

    comment_id = generate_id("wbc")
    
    response = {
        "id": comment_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "post_id": post_id,
        "metrics": {
            "likes": 0,
            "replies": 0
        },
        "status": "posted"
    }

    if media_urls:
        response["media"] = [
            {
                "type": "photo" if url.endswith(('.jpg','.png','.jpeg')) else "video",
                "url": url,
                "status": "processed"
            } for url in media_urls
        ]
    if reply_to_comment_id:
        response["in_reply_to_comment_id"] = reply_to_comment_id

    return response

# TikTok Functions
def post_tiktok(
    video_url: str,
    caption: Optional[str] = None,
    sound_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    allow_comments: bool = True,
    allow_duet: bool = True,
    allow_stitch: bool = True
) -> Dict[str, Any]:
    """
    Simulates posting a video on TikTok.
    
    Args:
        video_url: URL of the video file (required)
        caption: Video caption (optional, max 150 characters)
        sound_id: ID of background sound (optional)
        tags: List of hashtags (optional)
        allow_comments: Whether to allow comments (optional)
        allow_duet: Whether to allow duets (optional)
        allow_stitch: Whether to allow stitch (optional)
    
    Returns:
        Dict containing post details or error message
    """
    if not video_url:
        return {"error": "Video URL is required"}
    if not video_url.endswith(('.mp4', '.mov')):
        return {"error": "Invalid video format"}
    if caption and len(caption) > 150:
        return {"error": "Caption exceeds 150 characters"}

    post_id = generate_id("tt")
    
    response = {
        "id": post_id,
        "created_at": get_current_timestamp(),
        "video_url": video_url,
        "metrics": {
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "views": 0
        },
        "settings": {
            "comments_enabled": allow_comments,
            "duet_enabled": allow_duet,
            "stitch_enabled": allow_stitch
        },
        "status": "processing"  # TikTok typically processes videos
    }

    if caption:
        response["caption"] = caption
    if sound_id:
        response["sound"] = {"id": sound_id}
    if tags:
        response["hashtags"] = tags

    return response

def post_tiktok_comment(
    video_id: str,
    content: str,
    reply_to_comment_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on a TikTok video.
    """
    if not video_id:
        return {"error": "Video ID is required"}
    if not content:
        return {"error": "Comment content is required"}
    if len(content) > 150:
        return {"error": "Comment exceeds 150 characters"}

    comment_id = generate_id("ttc")
    
    response = {
        "id": comment_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "video_id": video_id,
        "metrics": {
            "likes": 0,
            "replies": 0
        },
        "status": "posted"
    }

    if reply_to_comment_id:
        response["in_reply_to_comment_id"] = reply_to_comment_id

    return response

# YouTube Functions
def post_youtube_video(
    video_url: str,
    title: str,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    category_id: str = "22",  # Default: People & Blogs
    privacy_status: str = "public",
    made_for_kids: bool = False
) -> Dict[str, Any]:
    """
    Simulates uploading a video to YouTube.
    
    Args:
        video_url: URL of the video file (required)
        title: Video title (required, max 100 characters)
        description: Video description (optional, max 5000 characters)
        tags: List of video tags (optional, max 500 characters total)
        category_id: Video category ID (optional)
        privacy_status: Privacy setting (optional: "public", "unlisted", "private")
        made_for_kids: Whether the video is made for kids (optional)
    
    Returns:
        Dict containing video details or error message
    """
    if not video_url or not title:
        return {"error": "Video URL and title are required"}
    if len(title) > 100:
        return {"error": "Title exceeds 100 characters"}
    if description and len(description) > 5000:
        return {"error": "Description exceeds 5000 characters"}
    if tags and sum(len(tag) for tag in tags) > 500:
        return {"error": "Total tags length exceeds 500 characters"}

    video_id = generate_id("yt")
    
    response = {
        "id": video_id,
        "created_at": get_current_timestamp(),
        "video_url": video_url,
        "title": title,
        "metrics": {
            "views": 0,
            "likes": 0,
            "comments": 0
        },
        "status": {
            "privacy": privacy_status,
            "upload": "processing",
            "made_for_kids": made_for_kids
        }
    }

    if description:
        response["description"] = description
    if tags:
        response["tags"] = tags
    if category_id:
        response["category_id"] = category_id

    return response

def post_youtube_comment(
    video_id: str,
    content: str,
    reply_to_comment_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on a YouTube video.
    
    Args:
        video_id: ID of the video to comment on (required)
        content: Comment text content (required, max 10000 characters)
        reply_to_comment_id: ID of comment being replied to (optional)
    
    Returns:
        Dict containing comment details or error message
    """
    if not video_id:
        return {"error": "Video ID is required"}
    if not content:
        return {"error": "Comment content is required"}
    if len(content) > 10000:
        return {"error": "Comment exceeds 10000 characters"}

    comment_id = generate_id("ytc")
    
    response = {
        "id": comment_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "video_id": video_id,
        "metrics": {
            "likes": 0,
            "replies": 0
        },
        "status": "published"
    }

    if reply_to_comment_id:
        response["in_reply_to_comment_id"] = reply_to_comment_id

    return response

# Bilibili Functions
def post_bilibili_video(
    video_url: str,
    title: str,
    partition_id: str,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    cover_url: Optional[str] = None,
    copyright_type: int = 1,  # 1: Original, 2: Repost
    thread_id: Optional[str] = None  # For series/collections
) -> Dict[str, Any]:
    """
    Simulates uploading a video to Bilibili.
    
    Args:
        video_url: URL of the video file (required)
        title: Video title (required, max 80 characters)
        partition_id: Video partition/category ID (required)
        description: Video description (optional, max 2000 characters)
        tags: List of video tags (optional, max 12 tags)
        cover_url: URL of video cover image (optional)
        copyright_type: Copyright type (optional, 1: Original, 2: Repost)
        thread_id: Series/collection ID (optional)
    
    Returns:
        Dict containing video details or error message
    """
    if not all([video_url, title, partition_id]):
        return {"error": "Video URL, title, and partition ID are required"}
    if len(title) > 80:
        return {"error": "Title exceeds 80 characters"}
    if description and len(description) > 2000:
        return {"error": "Description exceeds 2000 characters"}
    if tags and len(tags) > 12:
        return {"error": "Maximum 12 tags allowed"}

    video_id = generate_id("bv")  # Bilibili uses "BV" prefix for video IDs
    
    response = {
        "id": video_id,
        "created_at": get_current_timestamp(),
        "video_url": video_url,
        "title": title,
        "partition_id": partition_id,
        "copyright": copyright_type,
        "metrics": {
            "play": 0,
            "danmaku": 0,  # 弹幕数
            "like": 0,
            "coin": 0,
            "favorite": 0,
            "share": 0,
            "reply": 0
        },
        "status": {
            "upload": "processing",
            "review": "pending"  # Bilibili has content review process
        }
    }

    if description:
        response["description"] = description
    if tags:
        response["tags"] = tags
    if cover_url:
        response["cover_url"] = cover_url
    if thread_id:
        response["thread_id"] = thread_id

    return response

def post_bilibili_comment(
    video_id: str,
    content: str,
    reply_to_comment_id: Optional[str] = None,
    include_danmaku: bool = False,
    danmaku_settings: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates posting a comment on a Bilibili video.
    
    Args:
        video_id: ID of the video to comment on (required)
        content: Comment text content (required, max 1000 characters)
        reply_to_comment_id: ID of comment being replied to (optional)
        include_danmaku: Whether to send as danmaku (optional)
        danmaku_settings: Settings for danmaku (optional, e.g., position, color)
    
    Returns:
        Dict containing comment details or error message
    """
    if not video_id:
        return {"error": "Video ID is required"}
    if not content:
        return {"error": "Comment content is required"}
    if len(content) > 1000:
        return {"error": "Comment exceeds 1000 characters"}

    comment_id = generate_id("bc")
    
    response = {
        "id": comment_id,
        "created_at": get_current_timestamp(),
        "text": content,
        "video_id": video_id,
        "metrics": {
            "likes": 0,
            "replies": 0
        },
        "status": "published"
    }

    if reply_to_comment_id:
        response["in_reply_to_comment_id"] = reply_to_comment_id
    
    if include_danmaku:
        default_danmaku = {
            "position": "scroll",  # scroll, top, bottom
            "color": "#FFFFFF",
            "time": 0.0  # timestamp in video
        }
        danmaku_config = {**default_danmaku, **(danmaku_settings or {})}
        response["danmaku"] = {
            "id": generate_id("dm"),
            "settings": danmaku_config
        }

    return response