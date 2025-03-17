# AI Powered Recipe Chatbot

### Getting started.
Project built to solve the challenge: https://pressw.notion.site/Technical-Assessment-AI-Powered-Recipe-Chatbot-1b69b69f75be80dfb3e7fff9534449fb

Install via Poetry
```bash
poetry install
```

Run AI Powered chatbot
```bash
 uvicorn main:app --reload
 ```

Docker - PENDING

## Variable definition order
Environment variables take precedence over variables defined in the .env. If an environment variable and an .env variable have the same name the environment variable will be used.

### .env file
Refer to the versioned .env-example file for creating a local .env fileBefore execute the model, make sure you created .env file including the variables SERPAPI_API_KEY, and OPENAI_API_KEY

### Export the .env file as environment variables in the terminal
The .env file can be loaded as environment variables within a terminal using this command:
```bash
export $(cat .env | xargs)
```
