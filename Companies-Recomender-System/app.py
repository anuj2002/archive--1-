from flask import Flask, request, render_template
import pandas as pd

# Assuming 'data' is your dataset
data = pd.read_csv('companies-clean-data.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        # Extract form data
        rating = float(request.form.get('rating', 0.0))
        age_input = request.form.get('age', '')
        age = float(age_input) if age_input else 0.0
        company_type = request.form.get('company_type', None)
        
        # Extract positive attributes
        positive_attributes = {}
        positive_attribute_names = ['pos_work_life_balance', 'pos_company_culture', 'pos_appraisal', 'pos_learning',
                                    'pos_work_satisfaction', 'pos_salary_benefits', 'pos_promotions', 'pos_job_security',
                                    'pos_skill_development']
        for attribute_name in positive_attribute_names:
            positive_attributes[attribute_name] = int(request.form.get(attribute_name, 0))
        
        # Extract negative attributes
        negative_attributes = {}
        negative_attribute_names = ['con_work_life_balance', 'con_company_culture', 'con_appraisal', 'con_learning',
                                    'con_work_satisfaction', 'con_salary_benefits', 'con_promotions', 'con_job_security',
                                    'con_skill_development']
        for attribute_name in negative_attribute_names:
            negative_attributes[attribute_name] = int(request.form.get(attribute_name, 0))
        
        # Call recommendation_system function with form data
        recommended_companies = recommendation_system(rating=rating, age=age, company_type=company_type,
                                                      positive_attributes=positive_attributes,
                                                      negative_attributes=negative_attributes)
        return render_template('results.html', recommended_companies=recommended_companies)


def recommendation_system(company=None, company_type=None, rating=0.0, reviewers=0, age=0.0,
                          positive_attributes=None, negative_attributes=None):
    # Filter the dataset based on input parameters
    filtered_data = data
    
    if company:
        filtered_data = filtered_data[filtered_data['company'] == company]
    filtered_data = data
    if company_type:
        filtered_data = filtered_data[filtered_data['type'].str.contains(company_type)]
    if rating:
        filtered_data = filtered_data[filtered_data['rating'] >= rating]
    if reviewers:
        filtered_data = filtered_data[filtered_data['reviewers'] >= reviewers]
    if age:
        filtered_data = filtered_data[filtered_data['age'] >= age]
    
    # Filter based on positive attributes
    if positive_attributes:
        for attribute, value in positive_attributes.items():
            if value and attribute in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[attribute] == 1]
    
    # Filter based on negative attributes
    if negative_attributes:
        for attribute, value in negative_attributes.items():
            if value and attribute in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[attribute] == 0]
    
    # Return recommended companies based on filtered data
    recommendations = filtered_data['company'].unique()
    
    return recommendations


if __name__ == '__main__':
    app.run(debug=True)
