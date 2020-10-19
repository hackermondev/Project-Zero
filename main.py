from utils import database
from utils import language

import repltalk
import asyncio
from markdown import markdown
from parser import parse_html
from scan import scan_url
import os


import time 
from extra import *
from spam import get_score

import threading
import keepalive


def scan_recent_posts():
    r = asyncio.run(get_new_posts(limit=40))

    for post in r:
        if database.get(post.id) != None:
            return

        # if language.detect(post.content) != 'en':
        #   tr = language.translate(post.content).text
        #   database.set(post.id, True)
          
        #   asyncio.run(report_post(
        #             post,
        #             f'Please remember that only english is allowed on repl.it! \nTranslated: {tr}'))
          
        #   return

        score = get_score(post.content)

        if score < -20:
            asyncio.run(
                report_post(
                    post,
                    f'This post has been considered spam. Score: {score}'))
            
            database.set(post.id, True)
            asyncio.run(
                reply_to_post(
                    post,
                    f'This post has been considered spam. Score: {score}\n\nSpamming on repl.it is against the [rules](https://repl.it/talk/announcements/Repl-Talk-Rules-and-Guidelines-README/22109).'
                ))

            return

        c = markdown(post.content)

        r = parse_html(c)

        for link in r['links']:
            sc = scan_url(link)

            if sc['bad'] == True:
                asyncio.run(
                    report_post(
                        post,
                        f'This link was found in the post. It was scanned and was detected as suspicious. {link}'
                    ))

                database.set(post.id, True)

                print(f'This link is bad: {link}')

	
def commands_handler():
    c = asyncio.run(get_recent_comments())

    for commentt in c:
        if database.get(commentt.id) != None:
            return

        comment = commentt.content.lower()

        if comment.startswith('@projectzero'):
            command = comment.split()[1]

            if command == 'whois':
                try:
                    user = comment.split()[2]
                except IndexError:
                    user = commentt.author.name

                if user.startswith('@'):
                    user = user.replace('@', '')

                u = asyncio.run(get_user(user))

                
                database.set(commentt.id, True)
                asyncio.run(
                    reply_to_comment(
                        commentt,
                        f"![avatar](https://img.jdaniels.me/proxy?url={u.avatar})\n Name: {u.first_name} {u.last_name}\nUsername: {u.name}\nID: {u.id}\nBio: ```{u.bio}```"
                    ))
            elif command == 'replpedia':
                try:
                    entry = comment.split()[2]
                except IndexError:
                    entry = "replpedia"

                results = get_replpedia(entry)

                if results == False:
                    database.set(commentt.id, True)
                    asyncio.run(
                        reply_to_comment(
                            commentt,
                            "An error occured or the wiki couldn't be found"))

                try:
                    r = results[0]
                except KeyError:
                    database.set(commentt.id, True)
                    asyncio.run(
                        reply_to_comment(
                            commentt, 'That wiki was not found on replpedia'))

                database.set(commentt.id, True)
                asyncio.run(
                    reply_to_comment(
                        commentt,
                        f'Wiki found on replpedia!\n\n[{r["name"]}](https://replpedia.jdaniels.me/wiki/{r["name"]}) by {r["author"]}'
                    ))
            elif command == 'repldex':
                try:
                    entry = comment.split()[2]
                except IndexError:
                    database.set(commentt.id, True)
                    asyncio.run(
                        reply_to_comment(commentt,
                                         f'You didn\'t enter a query'))

                results = get_repldex(entry)

                if results == False:
                    database.set(commentt.id, True)
                    asyncio.run(
                        reply_to_comment(
                            commentt,
                            "An error occured or the entry couldn't be found"))

                try:
                    r = results[0]
                except KeyError:
                    database.set(commentt.id, True)
                    asyncio.run(
                        reply_to_comment(
                            commentt, 'That entry was not found on repldex'))

                database.set(commentt.id, True)
                asyncio.run(
                    reply_to_comment(
                        commentt,
                        f'Entry found on repldex!\n\n[{r["title"]}]\n{r["markdown"]}'
                    ))
            elif command == 'checkspam':

                return
                pc = post.content

                ouput = ''

                score = get_score(pc)

                if score < -20:
                    output = 'spam'
                else:
                    output = 'not spam'

                database.set(commentt.id, True)
                asyncio.run(
                    reply_to_comment(
                        commentt,
                        f'This post has been considered **{output}**. \nThe score is {score}'
                    ))


def scan_recent_comments():
    r = asyncio.run(get_recent_comments())

    for comment in r:
        c = markdown(comment.content)

        score = get_score(comment.content)

        if score < -20:
            database.set(comment.id, True)
            asyncio.run(
                report_comment(
                    comment,
                    f'This comment has been considered spam. Score: {score}'))
            
            asyncio.run(
                reply_to_comment(
                    comment,
                    f'This comment has been considered spam. Score: {score}\n\nSpamming on repl.it is against the [Rules](https://repl.it/talk/announcements/Repl-Talk-Rules-and-Guidelines-README/22109).'
                ))

            return

            r = parse_html(c)

            for link in r['links']:
                sc = scan_url(link)

                if sc['bad'] == True:

                    print(f'This link is bad: {link}')
                    asyncio.run(
                        report_comment(
                            post,
                            f'This link was found in the comment. It was scanned and was detected as suspicious. {link}'
                        ))

                    database.set(comment.id, True)


def detect_bots_accounts_on_recent_posts():
    # r = asyncio.run(get_new_posts(limit=20))

    r = asyncio.run(get_post(51877))

    print(r.title)


asyncio.run(login())

while True:
		# print('Scanning posts and comments...')

		ct = threading.Thread(target=commands_handler)

		ct.start()

		srp = threading.Thread(target=scan_recent_posts)

		srp.start()

		src = threading.Thread(target=scan_recent_comments)

		src.start()
		
		time.sleep(5)

