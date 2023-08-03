const express = require('express');
const { spawn } = require('child_process');

const app = express();
const port = 3000; 
app.use(express.json());

// Define the endpoint to handle user input
app.post('/execute-python', (req, res) => {
  const userInput = req.body.input;
  const pythonProcess = spawn('python3', ['python.py', userInput]);

  let output = '';

  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
    console.log(output);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
  });
  
  pythonProcess.on('close', (code) => {
    res.json({ output });
  });
});

app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});
