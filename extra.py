import repltalk
import os

import requests

client = repltalk.Client()

debug = True

requiredPosts = ["58598"]

async def login():
  await client.login('ProjectZero', os.getenv('PASSWORD'))
  print('I am logged in to repltalk.')

async def get_recent_comments(board="all"):
	p = []
	c = []

	if board != 'all':
		board = client.boards.ask

		async for posts in board.get_posts(sort="new", search="", limit=40):
			p.append(posts)
	else:
		async for posts in client.boards.all.get_posts(sort="new", search="", limit=40):
			p.append(posts)
		
	for pa in requiredPosts:
		poo = await client.get_post(pa)

		p.append(poo)
	
	for post in p:
		comments = await post.get_comments()

		for comment in comments:
			c.append(comment)

	return c
    
async def get_new_posts(limit=10):
    p = []

    async for posts in client.boards.all.get_posts(
            sort="new", search="", limit=limit):
        p.append(posts)

    return p

def get_repldex(search):
	b = requests.get(f'https://repldex.com/api/entry/{search}')

	if b.status_code == 500:
		return False

	j = b.json()
	
	return [j]

def get_replpedia(search):
	b = requests.post('https://replpedia.jdaniels.me/api/search', json={'search': search})

	j = b.json()
	
	if j['ok'] == False:
		return False
	
	return j['results']


async def get_post(id):
    p = await client.get_post(id)
    return p

async def reply_to_comment(comment, c):
	if debug:
		print(comment)
		print(c)

	await comment.reply(c)

async def reply_to_post(post, c):
		if debug:
			print(post)
			print(c)
			
		await post.post_comment(c)

async def get_user(username):
	u = await client.get_user(username)

	return u

async def report_post(post, reason):
    # await post.report(reason)
    print(post)
    print(reason)

    return {}

async def report_comment(comment, reason):
    # await comment.report(reason)
    print(comment)
    print(reason)

    return {}

async def get_comments(post):
    return await post.get_comments(order='new')