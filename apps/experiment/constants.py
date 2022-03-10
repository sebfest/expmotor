defaults = {'registration_help': """<p> This page lets you register for the experiment.</p>
<p> You need to chose the session you would like to take part in and fill out the rest of hte registration form.</p>
""",
            'confirmation_request_email': """
You have registered for an experiment using "Expmotor". 

Please confirm your email address by clicking on this link: 
    
<a href="{{ registration_link }}">Click here"</a>    

    
This is an auto-generated email.
""",
            'final_instructions_email': """We confirm your participation in the experiment.
    
You are registered for participation on {{ date }}, {{ time }} at {{ place }}.

The research group is grateful for your contribution,
and it is important to us that you take part. 

Should you need to cancel, or get in touch with us for
some other reason, you can do so by email to {{ email }},
or contact {{ manager }} by phone: {{ phone }}. 

On behalf of the research group,
{{ manager| title }}.
"""}

