<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Movie Collection API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            padding: 20px;
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #343a40;
        }
        code {
            background-color: #e9ecef;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

<h1>Django Movie Collection API</h1>

<p>This is a Django project that provides an API for managing movie collections. It includes features for creating, updating, and deleting collections and movies, as well as a request counting middleware.</p>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#running-the-project">Running the Project</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#running-tests">Running Tests</a></li>
    <li><a href="#contributing">Contributing</a></li>
</ul>

<h2 id="requirements">Requirements</h2>
<ul>
    <li>Python 3.x</li>
    <li>Django 5.1.2</li>
    <li>Django REST framework 3.15.2</li>
</ul>

<h2 id="installation">Installation</h2>
<ol>
    <li><strong>Clone the repository</strong>:
        <pre><code>git clone https://github.com/RequiemxOP/OneFin-Backend-Assignment
cd Django</code></pre>
    </li>
    <li><strong>Create a virtual environment</strong>:
        <pre><code>python -m venv venv</code></pre>
    </li>
    <li><strong>Activate the virtual environment</strong>:
        <ul>
            <li>On Windows:
                <pre><code>venv\Scripts\activate</code></pre>
            </li>
            <li>On macOS/Linux:
                <pre><code>source venv/bin/activate</code></pre>
            </li>
        </ul>
    </li>
    <li><strong>Install the required packages</strong>:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
</ol>

<h2 id="running-the-project">Running the Project</h2>
<ol>
    <li><strong>Apply migrations</strong>:
        <pre><code>python manage.py migrate</code></pre>
    </li>
    <li><strong>Run the development server</strong>:
        <pre><code>python manage.py runserver</code></pre>
    </li>
    <li><strong>Access the API</strong>:
        <p>Open your browser and navigate to <code>http://localhost:8000/</code> to see the API documentation or use an API client (like Postman) to test the endpoints.</p>
    </li>
</ol>

<h2 id="api-endpoints">API Endpoints</h2>
<ul>
    <li><strong>Create a Collection</strong>: <code>POST /collection/</code></li>
    <li><strong>Get Collections</strong>: <code>GET /collection/</code></li>
    <li><strong>Update a Collection</strong>: <code>PUT /collection/&lt;collection_uuid&gt;/</code></li>
    <li><strong>Delete a Collection</strong>: <code>DELETE /collection/&lt;collection_uuid&gt;/</code></li>
    <li><strong>Request Count</strong>: 
        <ul>
            <li>Get count: <code>GET /request-count/</code></li>
            <li>Reset count: <code>POST /request-count/reset/</code></li>
        </ul>
    </li>
</ul>

<h2 id="running-tests">Running Tests</h2>
<p>To run the tests, use the following command:</p>
<pre><code>python manage.py test</code></pre>

<h2 id="contributing">Contributing</h2>
<p>Feel free to submit issues or pull requests for any features or fixes.</p>

</body>
</html>
