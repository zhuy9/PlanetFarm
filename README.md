# PlanetFarm
### Abstract

Planet Farm is an interactive app that allows you to add different kinds of animals to your farm. These animals will move around randomly. If one predator collides with its prey, the prey will disappear. Besides animals, you can also add fences, or grasses to the farm.

### Usage
After you clone the project, navigate to the PlanetFarm folder
```
cd PlanetFarm
```
Create your venv
```
python3 -m venv venv
```
Run the venv
```
source venv/bin/activate
```
Run the server
```
python3 manage.py runserver
```
Navigate to your web browser, and go to: ``` http://127.0.0.1:8000/ ```

### Available commands
These animals will be recongnized by the app
```
['wolf', 'sheep', 'rabbit', 'snake', 'eagle']
```
Besides animals, these objects will also be recongnized
```
['wall', 'fence', 'grass']
```
