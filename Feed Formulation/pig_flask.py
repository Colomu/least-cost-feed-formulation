from flask import Flask, request, jsonify, render_template
from pig_formulation import get_formulation, ingredient_db  # Import ingredient_db and get_formulation

app = Flask(__name__)

@app.route('/')
def home():
    """
    Renders the home page with form options for feed formulation.
    """
    ingredient_options = {
        'energy_sources': [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'source'],
        'energy_replacers': [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'replacer'],
        'high_protein_sources': [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'high'],
        'medium_protein_sources': [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'medium'],
        'protein_replacers': [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'replacer']
    }

    return render_template('index.html', ingredient_options=ingredient_options)

@app.route('/formulate', methods=['POST'])
def formulate():
    """
    API endpoint to handle feed formulation requests.
    Validates input and calls get_formulation to generate formulations.
    """
    data = request.json

    # Debugging: Log the received data
    print("Received data:", data)

    try:
        # Check if categories are skipped and adjust accordingly
        energy_sources = data['energy_sources'] if data['energy_sources'] else []
        energy_replacers = data['energy_replacers'] if data['energy_replacers'] else []
        high_protein_sources = data['high_protein_sources'] if data['high_protein_sources'] else []
        medium_protein_sources = data['medium_protein_sources'] if data['medium_protein_sources'] else []
        protein_replacers = data['protein_replacers'] if data['protein_replacers'] else []

        # Ensure mandatory categories have at least two items if not skipped
        if (len(energy_sources) < 2 and len(data['energy_sources']) > 0) or \
           (len(energy_replacers) < 2 and len(data['energy_replacers']) > 0) or \
           (len(high_protein_sources) < 2 and len(data['high_protein_sources']) > 0) or \
           (len(medium_protein_sources) < 2 and len(data['medium_protein_sources']) > 0) or \
           (len(protein_replacers) < 2 and len(data['protein_replacers']) > 0):
            return jsonify({
                'error': "Each category must either be skipped or have at least two items selected."
            }), 400

        # Call the feed formulation logic
        formulations = get_formulation(
            pig_class=data['pig_class'],
            energy_sources=energy_sources,
            energy_replacers=energy_replacers,
            high_protein_sources=high_protein_sources,
            medium_protein_sources=medium_protein_sources,
            protein_replacers=protein_replacers
        )

        # Debugging: Log the generated formulations
        print("Formulations generated:", formulations)

        return jsonify({'formulations': formulations})

    except Exception as e:
        print(f"Error in formulation process: {str(e)}")
        return jsonify({'error': 'An error occurred during formulation.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
