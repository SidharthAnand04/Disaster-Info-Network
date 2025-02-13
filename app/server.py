from flask import Flask, render_template, request, jsonify, url_for
import csv
import os

app = Flask(__name__)

# Path to CSV file
CSV_FILE = os.path.join('data', 'damage_reports.csv')

def read_damage_reports():
    """
    Read damage reports from CSV file and return as a list of dicts.
    Each dict has: report_type, location, description, severity
    """
    if not os.path.exists(CSV_FILE):
        return []
    
    data = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            loc = row['location'].strip()
            if loc.startswith('(') and loc.endswith(')'):
                loc = loc[1:-1]
            row['location'] = loc
            data.append(row)
    return data

def append_damage_report(report_type, location, description, severity):
    """
    Append a new damage report entry to the CSV file.
    CSV columns: report_type, location, description, severity
    """
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['report_type', 'location', 'description', 'severity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        cleaned_location = location.strip()
        if cleaned_location.startswith('(') and cleaned_location.endswith(')'):
            cleaned_location = cleaned_location[1:-1]
        
        writer.writerow({
            'report_type': report_type,
            'location': cleaned_location,
            'description': description,
            'severity': severity
        })

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/report', methods=['GET', 'POST'])
def report_damage():
    if request.method == 'GET':
        return render_template('report_damage.html')
    else:
        report_type = request.form.get('report_type')
        location = request.form.get('location')
        description = request.form.get('description')
        severity = request.form.get('severity')
        
        append_damage_report(report_type, location, description, severity)
        return "Report submitted successfully! Go Back to Home Page <a href='/'>Home</a>"

@app.route('/map')
def view_map():
    return render_template('view_map.html')

@app.route('/api/damage_reports', methods=['GET'])
def get_damage_reports():
    data = read_damage_reports()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
