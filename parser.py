from bs4 import BeautifulSoup

# This file will parser the markdown and return images, links, etc

def parse_html(html):
  soup = BeautifulSoup(html, 'html.parser')

  links = []
  images = []

  for image in soup.find_all('img'):
    if image['src'] == None:
      continue
    else:
      images.append(image['src'])

  for a in soup.find_all('a'):
    if a['href'] == None:
      continue
    else:
      links.append(a['href'])

  return { 'links': links, 'images': images}