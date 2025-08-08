from flask import Flask, jsonify, request, render_template, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Prize configuration with the exact percentages you specified
PRIZES = [
    {"name": "10000₹", "chance": 0},
    {"name": "1000₹", "chance": 0},
    {"name": "500₹", "chance": 0},
    {"name": "200₹", "chance": 0},
    {"name": "100₹", "chance": 5},
    {"name": "50₹", "chance": 10},
    {"name": "10₹", "chance": 30},
    {"name": "Better Luck Next Time", "chance": 60}
]

@app.route('/')
def index():
    # Check if user has already spun
    has_spun = session.get('has_spun', False)
    prize = session.get('prize', None)
    return render_template('index.html', prizes=PRIZES, has_spun=has_spun, prize=prize)

@app.route('/spin', methods=['POST'])
def spin_wheel():
    # Check if user has already spun
    if session.get('has_spun', False):
        return jsonify({
            "error": "You have already participated in this giveaway.",
            "prize": session.get('prize', None)
        }), 400
    
    # Mark user as having spun
    session['has_spun'] = True
    
    # Select a prize based on weights
    weights = [prize["chance"] for prize in PRIZES]
    selected_prize = random.choices(PRIZES, weights=weights, k=1)[0]
    prize_index = PRIZES.index(selected_prize)
    
    # Store the prize in session
    session['prize'] = selected_prize
    
    # Calculate the rotation needed to land on the selected prize
    angle_per_section = 360 / len(PRIZES)
    target_angle = 3600 - (prize_index * angle_per_section) + (angle_per_section / 2)
    
    return jsonify({
        "prize": selected_prize,
        "rotation": target_angle
    })

if __name__ == '__main__':
    app.run(debug=True)
