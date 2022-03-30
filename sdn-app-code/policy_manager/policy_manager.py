import asyncio
from flask import Flask

app = Flask(__name__)

# create thread pool

async def add_policy():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

# Begin managing new policy
@app.route("/policy", methods=["POST"])
def create_policy():
    
    asyncio.run(add_policy())
    return

# Remove policy from managed policies
@app.route("/policy", methods=["DELETE"])
def delete_policy():

    return

app.config.update(SESSION_COOKIE_NAME="policy_manager")
app.run(host='0.0.0.0',port=5050)