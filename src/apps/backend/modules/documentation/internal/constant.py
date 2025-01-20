DOCUMENTATION_GENERATION_PROMPT = (
    "Generate a detailed and accurate API documentation in a human-readable bullet pointed markdown format "
    "with proper spacing and indentation for the routes provided. The documentation should include the following "
    "for each route: a clear description, endpoint, HTTP method, request body parameters (with all possible variations "
    "stated clearly in sections with proper titles), and response status code & body parameters. Ensure that the request "
    "and response bodies attributes are accurately defined, using variable names as defined in the service method "
    "parameter of the controller method in case of request and serializers in case of response. Make sure to include only "
    "the variable names in the request and response bodies, not the types or other details. Also make sure to categorize "
    "the routes into sections with proper titles. Return the documentation as a markdown file, without any additional text "
    "or comments like adding ```markdown at the beginning or at the end. Add underlines b/w each route of the section like "
    "(---) in the generated markdown file, but not under the title of the section or under the last route of the section."
)
