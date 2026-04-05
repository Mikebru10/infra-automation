from flask import Flask, request, render_template_string, send_file
import subprocess
import os

app = Flask(__name__)

HTML = """
<h2>Prompt Optimizer</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <select name=profile>
    <option value=technical-only>Technical Only</option>
    <option value=full-context>Full Context</option>
  </select>
  <input type=submit value=Upload>
</form>
"""

@app.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        profile = request.form['profile']
        path = f"/data/input/{f.filename}"
        f.save(path)
        subprocess.run([
            "python3","/repo/scripts/generate_prompt_artifact.py",
            "--input", path,
            "--profile", profile,
            "--mode", "ollama",
            "--ollama-url", os.getenv("OLLAMA_URL"),
            "--output-dir", "/data/output"
        ])
        return "Processed. Check output directory."
    return render_template_string(HTML)

app.run(host='0.0.0.0', port=8080)
