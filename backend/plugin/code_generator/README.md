> [!TIP]
> The current version only includes backend code generation.

> [!WARNING]
> Since jinja2 outputs templates as plain text, formatting issues may occur. Therefore, the `preview` endpoint might not display code intuitively—this is a preset for frontend use.

## Introduction

The code generator is implemented via API calls and includes two modules. The design may have flaws; please submit issues for any problems.

### 1. Code Generation Business

Contains configuration related to code generation. For details, see: `generator/model/gen_business.py`

### 2. Code Generation Model Columns

Contains the model column information required for code generation, similar to defining model columns normally. Currently, supported features are limited.

## Usage

1. Start the backend service and use the Swagger documentation directly.
2. Send API requests using third-party debugging tools.
3. Start both frontend and backend and operate from the web page.

Most API parameters are documented—please review them carefully.

### F. Manual Mode

Not recommended (manual business creation is marked as "deprecated").

1. Manually add a business entry via the business creation endpoint.
2. Manually add model columns via the model creation endpoint.
3. Use the `preview` (preview), `generate` (write to disk), and `download` (download) endpoints to perform backend code generation tasks.

### S. Automatic Mode

Recommended.

1. Use the `tables` endpoint to get a list of database table names.
2. Use the `import` endpoint to import existing database tables; this will automatically create business and model table data.
3. Use the `preview` (preview), `generate` (write to disk), and `download` (download) endpoints to perform backend code generation tasks.
