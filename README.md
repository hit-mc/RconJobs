# RconJobs

Write Minecraft command scripts for your server, in a Pythonic way.

## Usage

1. Clone this repository.

2. Ensure your python(>=3.8) environment is ready, and dependencies are satisfied.

3. Create a new `.py` file for your single new task in `tasks` folder.

4. Create a new class in that file, which inherits from `BaseTask` class in `jobs.py` (you have to `from jobs import BaseTask` in advance).

5. Override `run` method to define your script, and `should_run` method to schedule your task.

6. Create `rconjobs.json` in the same folder with `rconjobs.py` and configure it like this:

   ```json
   {
       "rcon": {
           "host": "192.168.1.2",
           "port": 25565,
           "password": "top_secret",
           "use_tls": false
       }
   }
   ```

7. Run `rconjobs.py`. Now it works!
