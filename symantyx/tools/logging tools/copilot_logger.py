import subprocess
import json
import time
 
from log import log_event

def log_copilot_interaction(prompt, response):
    ctx = {
        "client": "copilot-app",
        "domain": "desktop",
        "event": "interaction",
        "name": "copilot",
        "generation": str(int(time.time())),
    }

    fmt = "%t %c %d %e %g | prompt=%f | response=%m"
    log_event(fmt,
              client=ctx["client"],
              domain=ctx["domain"],
              event=ctx["event"],
              name=ctx["name"],
              generation=ctx["generation"],
              function=prompt,
              module=response)
