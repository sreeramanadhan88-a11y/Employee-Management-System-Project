from django.urls import path

from . import views


urlpatterns = [

    # Salary

    path(
        'salaries/',
        views.salary_list,
        name='salary_list'
    ),

    path(
        'salaries/add/',
        views.add_salary,
        name='add_salary'
    ),

    path(
        'salaries/<int:salary_id>/edit/',
        views.edit_salary,
        name='edit_salary'
    ),


    # Payments

    path(
        'payments/',
        views.payment_list,
        name='payment_list'
    ),

    path(
        'payments/add/',
        views.add_payment,
        name='add_payment'
    ),

    path(
        'payments/<int:payment_id>/edit/',
        views.edit_payment,
        name='edit_payment'
    ),


    # Bank Statements

    path(
        'bank-statements/',
        views.bank_statement_list,
        name='bank_statement_list'
    ),

    path(
        'bank-statements/add/',
        views.add_bank_statement,
        name='add_bank_statement'
    ),

    path(
        'bank-statements/<int:statement_id>/edit/',
        views.edit_bank_statement,
        name='edit_bank_statement'
    ),


    # Insurance

    path(
        'insurance/',
        views.insurance_list,
        name='insurance_list'
    ),

    path(
        'insurance/add/',
        views.add_insurance,
        name='add_insurance'
    ),

    path(
        'insurance/claim/submit/',
        views.submit_insurance_claim,
        name='submit_insurance_claim'
    ),

    path(
        'insurance/claims/',
        views.my_insurance_claims,
        name='my_insurance_claims'
    ),

    path(
        'insurance/claims/manage/',
        views.insurance_claim_list,
        name='insurance_claim_list'
    ),

    path(
        'insurance/claims/<int:claim_id>/approve/',
        views.approve_insurance_claim,
        name='approve_insurance_claim'
    ),

    path(
        'insurance/claims/<int:claim_id>/reject/',
        views.reject_insurance_claim,
        name='reject_insurance_claim'
    ),

]