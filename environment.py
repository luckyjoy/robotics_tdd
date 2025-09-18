from allure_behave.hooks import allure_report

def before_all(context):
    # Initialize Allure reporting
    allure_report("allure-results")
