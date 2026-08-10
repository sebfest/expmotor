# ExpMotor 
### Registration Software for Recruiting Participants 

---

This is the source code for ExpMotor which is currently in use at FAIR to help registering 
participants for scientific experiments. 

A live version of the website can currently be found [here](https://thomas.nhh.no/expmotor).

## Local development

Copy `.dev.example` to `.dev`, adjust the values if needed, and start the development
stack with `docker compose up --build`. Dependencies are managed by uv; run `uv sync`
for the development environment. The default local account is `admin` with
password `admin`. Fake data is opt-in: set `GENERATE_FAKE_DATA=1` in `.dev` when it
is wanted.

The test suite can be run without Postgres or Redis:

```shell
uv run pytest
```

&copy; Sebastian Fest, FAIR, 2023
