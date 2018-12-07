#!/usr/bin/python

import logging
import requests

tree_name = 'ACP_DataServices'
url = 'http://localhost:4242'
logging.basicConfig(level=logging.INFO, format='%(message)s')

logging.info("Checking existing OpenTSDB Trees")
resp = requests.get(url=url + '/api/tree')
data = resp.json()

treeId = None
for tree in data:
  logging.info(tree)
  if tree['name'] == tree_name:
    treeId = tree['treeId']
    break

if not treeId:
  logging.info('Creating new tree')
  params = {}
  params['name'] = tree_name
  params['method_override'] = 'post'
  params['storeFailures'] = 'true'

  resp = requests.post(url=url + '/api/tree', params=params)

  data = resp.json()
  logging.info('Tree created')
  logging.info(data)
  treeId = data['treeId']
  logging.info(treeId)

  post_data = [
    {
        "treeid": treeId,
        "level": 0,
        "order": 0,
        "type": "tagk",
        "field": "project",
        "description": "Project"
    },
    {
        "treeid": treeId,
        "level": 1,
        "order": 0,
        "type": "tagk",
        "field": "env",
        "description": "Environment"
    },
    {
        "treeid": treeId,
        "level": 2,
        "order": 0,
        "type": "tagk",
        "field": "region",
        "description": "Region"
    },
    {
        "treeid": treeId,
        "level": 3,
        "order": 0,
        "type": "METRIC",
        "description": "Metric"
    }
  ]
  
  logging.info('Using tree data:')
  for rule in post_data:
    logging.info(rule)
    resp = requests.put(url=url + '/api/tree/rule', params=rule)
    data = resp.json()

    logging.info(data)
else:
  logging.info('Tree with name {0} and id {1} already exists.'.format(tree_name, treeId))


