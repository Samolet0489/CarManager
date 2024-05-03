// Import necessary modules
const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');
const path = require('path'); // Import the path module

// Create Express app
const app = express();

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Define endpoint to handle creation of a new vehicle
app.post('/save-vehicle', (req, res) => {
    console.log('Received request to save vehicle');

    // Get the vehicle data from the request body
    const vehicle = req.body;

    console.log('Received vehicle data:', vehicle);

    // Load existing vehicles from JSON file (if any)
    let existingVehicles = [];
    try {
        // Read the existing JSON file
        const existingData = fs.readFileSync(path.join(__dirname, '..', 'temp_files', 'create_vehicle.json'), 'utf8');
        if (existingData.trim() !== '') {
            // Parse existing JSON data
            existingVehicles = JSON.parse(existingData);
        }
    } catch (error) {
        if (error.code !== 'ENOENT') {
            console.error('Error reading existing vehicles:', error);
            return res.status(500).json({ error: 'Failed to read existing vehicles' });
        }
    }

    // Add the new vehicle to the existing vehicles array
    existingVehicles.push(vehicle);

    // Write the updated vehicles array to the JSON file
    fs.writeFile(path.join(__dirname, '..', 'temp_files', 'create_vehicle.json'), JSON.stringify(existingVehicles, null, 2), (err) => {
        if (err) {
            console.error('Error saving vehicle:', err);
            return res.status(500).json({ error: 'Failed to save vehicle' });
        } else {
            console.log('Vehicle saved successfully');
            return res.status(200).json({ message: 'Vehicle saved successfully' });
        }
    });
});

// Serve the HTML file when accessing the root URL
app.get('/', (req, res) => {
    // Send the HTML file located in the 'templates' directory
    res.sendFile(path.join(__dirname, 'templates', 'create_vehicle.html'));
});

// Start the server
const PORT = process.env.PORT || 8080; // Change the port to 8080
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
