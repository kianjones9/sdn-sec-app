import threading
import time
from policy import RateLimitPolicy
from flask import Flask, request, jsonify

app = Flask(__name__)

# create "policy database"

policy_db = []

# = f'http://localhost:8181/onos/v1/flows/{deviceID}/{flowid}'
# Begin managing new policy
@app.route("/policy", methods=["POST"])
def create_policy():

    args = request.json

    threshold = args["threshold"]
    url = args["url"]
    
    policy = RateLimitPolicy(url, threshold)
    policy_db.append(policy)

    return "<p>policy added</p>"

# Remove policy from managed policies
@app.route("/policy", methods=["DELETE"])
def delete_policy():
    index = request.args["policy"]
    policy_db.pop(index)

    return "<p>policy deleted</p>"

# Check status of policies
@app.route("/policy", methods=["GET"])
def get_policies():

    policies = {}

    for x in range(len(policy_db)):
        policies[f"{x}"] = policy_db[x].triggered

    return jsonify(policies)


app.config.update(SESSION_COOKIE_NAME="policy_manager")


def policy_polling():
    
    while True:

        for policy in policy_db:
            
            policy.probe()
            print(policy.trigger.status)
        
        time.sleep(10)
    
policy_poller = threading.Thread(target=policy_polling)
policy_poller.start()

app.run(host='localhost',port=5550)
# policy_poller.cancel()