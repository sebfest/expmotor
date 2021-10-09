defaults = {
    'registration_help': """
<p> This page lets you register for the experiment.</p>
<p> You need to tick off the session you would like to take part in.</p>
""",
    'confirmation_request_email': """
You have registered for an experiment using "Expmotor". 

Please confirm your email address by clicking on this link: 
    
http://127.0.0.1:8000{% url 'experiment:registration_activate' uidb64=uid token=token  %}
    
This is an auto-generated email.
""",
    'final_instructions_email': """
We confirm your participation in the experiment.
    
You are registered for participation on {{ session.date }}, {{ session.time }} at {{ session.place }}.

The research group is grateful for your contribution,
and it is important to us that you take part. 

Should you need to cancel, or get in touch with us for
some other reason, you can do so by email to {{ manager.email }},
or contact {{ manager }} by phone: {{ manager.phone }}. 

On behalf of the research group,
{{ manager| title }}.
"""
}