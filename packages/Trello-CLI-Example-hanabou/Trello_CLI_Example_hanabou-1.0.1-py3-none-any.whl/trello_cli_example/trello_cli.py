"""TRELLO CLI

Usage:
    trello_cli.py add_card <NAME> --list=<LIST> [(--label_name=<LABEL_NAME> --label_color=<LABEL_COLOR>)...] [--comment=<COMMENT_TEXT>]
    trello_cli.py -h|--help
    trello_cli.py -v|--version

Arguments:
    NAME                              Name of the new Trello card
    --list=LIST                       Name of the list that will contain the new Trello card (todo, doing, done)
    --label_name=<LABEL_NAME>         Label name for the new Trello card
    --label_color=<LABEL_COLOR>       Label color for the new Trello card (yellow, purple, blue, red, green, orange, black, sky, pink, lime)
    --comment=<COMMENT_TEXT>          Text contents for a comment on the new Trello card

Options:
    -h --help  Show this screen
    -v --version  Show version

"""

from docopt import docopt
import requests
import sys
import json
from trello_cli_example.config import api_key, access_token
from trello_cli_example import urlCards, urlLabels, idBoard, idListDict, labelColorList


def post_card(name, idList, key=api_key, token=access_token, idLabels=None):
    response = requests.post(urlCards, 
        data = {'key': key, 'token': token, 'idList': idList, 'name': name, 'idLabels': idLabels})
    response.raise_for_status()
    data = response.json()
    idCard = data['id']
    return idCard


def post_label(name, color, key=api_key, token=access_token, idBoard=idBoard):
    response = requests.post(urlLabels, 
        data = {'key': key, 'token': token, 'idBoard': idBoard, 'name': name, 'color': color})
    response.raise_for_status()
    data = response.json()
    idLabel = data['id']
    return idLabel

def post_comment(text, idCard, key=api_key, token=access_token):
    urlComments = urlCards + '/{}/actions/comments'.format(idCard)
    response = requests.post(urlComments, 
        data = {'key': key, 'token': token, 'text': text})
    response.raise_for_status()
    data = response.json()
    idComment = data['id']
    return idComment


def main():
    args = docopt(__doc__, version='1.0.1')
    try:
        if(args['add_card']):

            if(args['--list'] not in idListDict):
                raise ValueError("List '{}' does not exist. Acceptable list names are: {} \n".format(args['--list'], list(idListDict.keys())))
            
            idLabelList = []
            if(args['--label_name']):
                for color in args['--label_color']:
                    if(color not in labelColorList):
                        raise ValueError("One or more label colors in '{}' do not exist. Acceptable label colors are: {} \n".format(args['--label_color'], labelColorList))
                for label in list(zip(args['--label_name'], args['--label_color'])):
                    idLabel = post_label(label[0], label[1])
                    idLabelList.append(idLabel)
            
            idCard = post_card(args['<NAME>'], idListDict[args['--list']], idLabels=idLabelList)

            if(args['--comment']):
                post_comment(args['--comment'], idCard)
    except requests.exceptions.HTTPError as e: 
        sys.stderr.write(str(e))
        sys.exit(1)
    except ValueError as e:
        sys.stderr.write(str(e))
        sys.exit(1)

if __name__=="__main__": 
    main() 