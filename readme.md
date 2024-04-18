
# Installation
1. Install Docker Desktop. This guide assumes that you have `docker-compose` cli installed on your system.
2. If you want to attach the terminal with the installation process of neural network, run:
   ```
   docker-compose up 
   ```
   Or if you want to run the installation in the background, run:
   ```
   docker-compose up -d
   ```
3. Install dependencies using:
   ```
   npm install
   ```
4. Once the installation is done and the neural net is running (you can check it in docker desktop), run the script using:
   ```
   npm start
   ```

# Executing the Script
## Regions
### 1. Creating the Schema
This region creates the schema definition for the vector database with the necessary data types and other requirements. This should be run at least once. You can comment this region later on.

### 2. Batch Imports
This region creates entries in the vector database for each image present in the "images/" folder. This should be run at least once, but can be run whenever your dataset needs to change in the vector database. If you don't want to run it, just comment it out.

### 3. Comparison
This region compares the images from the "input-images/" folder one by one with the images present in the vector database and returns you the matching image results.
