const express = require('express');
const { spawn } = require('child_process');
const app = express();
const port = 3000; // You can use any port you prefer

// Middleware to parse JSON data
app.use(express.json());

// Define the endpoint to handle user input
app.post('/execute-python', (req, res) => {
  const userInput = req.body.input; // Assuming the user input is sent as a JSON object with the "input" field
  // Spawn a new Python process and execute the script with user input as arguments
  const pythonProcess = spawn('python3', ['python.py', userInput]);

  let output = '';

  // Collect output from the Python script
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
    console.log(output);
  });

  // Handle Python script errors
  pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
  });
  
  // When the Python script finishes, send the output back to the user
  pythonProcess.on('close', (code) => {
    res.json({ output });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});
