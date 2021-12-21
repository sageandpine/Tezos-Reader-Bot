
# Tezos_Reader_Bot pulls a random pdf NFT from hic dex and displays it in discord chat with a link and info when 
# $read is called.
# Add more commands
#TO DO: Retrieve spoken word?
#To Do: Filter by tag
# To Do: Rate Limiting

import random
import os
import discord
from replit import db
from keep_alive import keep_alive
import requests
import json
import pandas as pd

my_secret = os.environ['bot-tots']
client  = discord.Client()

poetry = "poetry"
fiction = "fiction"
sci-fi = "sci-fi"
comic = "comic"


main_q = """query ObjktsByTag($tag1: String_comparison_exp = {_eq: "fiction"}) {
  hic_et_nunc_token(where: {mime: {_in: "application/pdf"}, token_tags: {tag: {tag: $tag1}}}, limit: 10) {
    id
  }
}
"""
def get_rand_pdf(number):
  """Returns a Random NFT PDF from the HicDex API."""
  query = main_q
  # post query to hicdex
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  # Convert to DataFrame
  df = pd.DataFrame(json_data)
  #Access token number and store in variable
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  # Format into a string to be returned by function
  #link_string = f"https://hen.radio/objkt/{df_objkt_id}"
  link_string = f"https://hic.art/{df_objkt_id}"
  print(link_string)
  return link_string


@client.event
async def on_ready():
  """Send message when bot logs on"""
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  """Defines action in Discord when bot recieves commands"""
  if message.author == client.user:
    return

  if message.content.startswith('$read'):
    num = random.randrange(0,10)
    rand_pdf = get_rand_pdf(num)
    #update_objkt_list(rand_music) 
    await message.channel.send(rand_pdf)

keep_alive()
client.run(my_secret)