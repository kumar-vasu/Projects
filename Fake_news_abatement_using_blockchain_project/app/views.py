import datetime
import json
import yaml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from flask import render_template, redirect, request
from flask_mysqldb import MySQL
from app import app
from string import Template


MY_ADDRESS = 'cursednarutouzumaki@gmail.com'
PASSWORD = 'Maverick@467'

proof_data={}
global query_number
query_number=0

db = yaml.load(open('E:\\New_folder - Copy\\python_blockchain_app-blockchain_post\\app\\db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
mysql = MySQL(app)
#cur = mysql.connection.cursor()
#cur.execute("INSERT INTO "NAME OF TABLE"(column names seperated by ",") VALUES(%S,%S,%S)TYPE OF DATA ,(VARIABLES IN .PY TO BE ALLOTED)")
#mysql.connection.commit()
#cur.close()
#code continues
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []
proof_object =[]


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def check_for_proof_requirement(post_content):
    check=False
    names, emails = get_contacts('hot_words.txt') # read contacts
    res = dict(zip(names, emails))
    names_found=[]
    line = post_content.split()
    for word in names:
        lower = word.lower()
        lower = lower.rstrip()
        count = 0
        for each in line:
            line2 = each.lower()
            line2 = line2.strip("!@#$%^&*()_-+=")
            if lower == line2:
                count+=1
        if count != 0:
            names_found.append(word)
            check=True
    return names_found , check , res



def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)



@app.route('/')
def index():
    fetch_posts()
    return render_template('index.php',
                           title='Blockchain App for sharing' ,
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/proofpage')
def proof_page():
    return render_template('proof.html')


@app.route('/proofpage/proof', methods=['POST','GET'])
def proof_textarea():
# end point to take proof from proof page and post to aap
    #if request.method == "POST":
        proof = request.form["content"]
        proofauthor = request.form["author"]
        certification = request.form["certify"]
        proofquery= request.form["proofquery"]

        cur = mysql.connection.cursor()
        result=cur.execute("SELECT * FROM transbchain WHERE query_number = %s",proofquery )
        if result > 0:
            dbcontent = cur.fetchall()
            print("2#####",dbcontent)

        global proof_object
        proof_object = {
            'author': dbcontent[0][0],
            'content': dbcontent[0][1],
            'proof_author': proofauthor,
            'proof_content': proof,
            'certification': certification
        }

        mysql.connection.commit()
        cur.close()
        new_tx_address = "{}/new_proof_transaction".format(CONNECTED_NODE_ADDRESS)
        requests.post(new_tx_address,
                      json=proof_object,
                      headers={'Content-type': 'application/json'})

        return redirect('/')

#endpoint to respond to get request from app and send proof
    #else:
       # return json.dumps(proof_object)

"""
def submit_after_proof():
    new_tx_address = "{}/new_proof_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                      json=proof_object,
                      headers={'Content-type': 'application/json'})

    return redirect('/')
"""
@app.route('/submit', methods=['POST','GET'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    #global query_number
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
        'proof_author': "",
        'proof_content': "",
        'certification': ""
    }

    final_list , proof_required , res=check_for_proof_requirement(post_content)
    #print(final_list)
    if proof_required is True:
        global query_number
        query_number+=1
        message_template = read_template('message_template.txt')
        for current in final_list:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login(MY_ADDRESS, PASSWORD)

            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=current.title(),QUERY_NUMBER=query_number)

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=res[current]
            msg['Subject']="This is TEST"

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg

            # Terminate the SMTP session and close the connection
            s.quit()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO transbchain(author , content , query_number ) VALUES(%s,%s,%s)",(post_object['author'],post_object['content'],query_number))
            mysql.connection.commit()
            cur.close()
            #increment querynumber
    # Submit a transaction
    else:
        new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
        requests.post(new_tx_address,
                      json=post_object,
                      headers={'Content-type': 'application/json'})

    return redirect('/')
    """
    if proof_object:
        post_object["proof_author"]=proof_object["proof_author"]
        post_object["proof_content"]=proof_object["proof_content"]
        post_object["certification"]=proof_object["certification"]
    """




def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
